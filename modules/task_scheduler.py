import heapq
from typing import List, Dict, Optional, Set
from models import MarketingTask

class TaskScheduler:
    def __init__(self):
        self.task_map: Dict[str, MarketingTask] = {}
        self.dependencies: Dict[str, Set[str]] = {}
        self.dependents: Dict[str, Set[str]] = {}
        self.completed_tasks: Set[str] = set()
        self.ready_heap: List[tuple] = []  # (priority, created_date, task_id)

    def _refresh_ready_heap(self):
        """重建最大堆，只包含所有依赖已完成的任务"""
        self.ready_heap = []
        for task_id, task in self.task_map.items():
            if task_id in self.completed_tasks:
                continue
            if all(dep in self.completed_tasks for dep in self.dependencies.get(task_id, set())):
                heapq.heappush(self.ready_heap, (-task.priority, task.created_date, task_id))

    def insert(self, task: MarketingTask):
        if task.id in self.task_map:
            raise ValueError(f"任务ID {task.id} 已存在")
        self.task_map[task.id] = task
        self.dependencies.setdefault(task.id, set())
        self.dependents.setdefault(task.id, set())
        self._refresh_ready_heap()

    def delete(self, task_id: str):
        if task_id not in self.task_map:
            raise ValueError("任务不存在")
        for dep in self.dependencies.get(task_id, set()):
            self.dependents[dep].discard(task_id)
        for dep in self.dependents.get(task_id, set()):
            self.dependencies[dep].discard(task_id)
        self.dependencies.pop(task_id, None)
        self.dependents.pop(task_id, None)
        self.task_map.pop(task_id)
        self.completed_tasks.discard(task_id)
        self._refresh_ready_heap()

    def update(self, task_id: str, **kwargs):
        if task_id not in self.task_map:
            raise ValueError("任务不存在")
        task = self.task_map[task_id]
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
        task.priority = task.urgency * task.influence
        self._refresh_ready_heap()

    def add_dependency(self, before_id: str, after_id: str):
        if before_id not in self.task_map or after_id not in self.task_map:
            raise ValueError("依赖的任务不存在")
        if before_id == after_id:
            raise ValueError("不能依赖自身")
        if self._has_path(after_id, before_id):
            raise ValueError("添加该依赖会导致环")
        self.dependencies[after_id].add(before_id)
        self.dependents[before_id].add(after_id)
        self._refresh_ready_heap()

    def remove_dependency(self, before_id: str, after_id: str):
        self.dependencies.get(after_id, set()).discard(before_id)
        self.dependents.get(before_id, set()).discard(after_id)
        self._refresh_ready_heap()

    def _has_path(self, start: str, end: str) -> bool:
        visited = set()
        stack = [start]
        while stack:
            node = stack.pop()
            if node == end:
                return True
            for dep in self.dependents.get(node, set()):
                if dep not in visited:
                    visited.add(dep)
                    stack.append(dep)
        return False

    def execute_highest_priority(self) -> Optional[MarketingTask]:
        self._refresh_ready_heap()
        while self.ready_heap:
            _, _, task_id = heapq.heappop(self.ready_heap)
            if task_id not in self.completed_tasks:
                self.completed_tasks.add(task_id)
                self._refresh_ready_heap()
                return self.task_map[task_id]
        return None

    def top_k_tasks(self, k: int) -> List[MarketingTask]:
        self._refresh_ready_heap()
        topk = heapq.nsmallest(k, self.ready_heap)
        return [self.task_map[task_id] for _, _, task_id in topk]

    def get_dependencies_graph(self):
        nodes = [{"id": tid, "label": self.task_map[tid].name} for tid in self.task_map]
        edges = []
        for after, befores in self.dependencies.items():
            for before in befores:
                if before in self.task_map and after in self.task_map:
                    edges.append({"from": before, "to": after})
        return {"nodes": nodes, "edges": edges}

    def get_task_statistics(self) -> Dict:
        total = len(self.task_map)
        completed = len(self.completed_tasks)
        pending = total - completed
        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": pending,
            "completion_rate": completed / total if total > 0 else 0
        }
