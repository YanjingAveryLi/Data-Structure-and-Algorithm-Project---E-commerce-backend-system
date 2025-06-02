import bisect

class LSMTree:
    def __init__(self, memtable_limit=5):
        self.memtable = []  # [(key, value)]，有序
        self.sstables = []  # 每个sstable是有序的[(key, value)]列表
        self.memtable_limit = memtable_limit

    def insert(self, key, value):
        # 插入到memtable，保持有序
        idx = bisect.bisect_left([k for k, _ in self.memtable], key)
        if idx < len(self.memtable) and self.memtable[idx][0] == key:
            self.memtable[idx] = (key, value)
        else:
            self.memtable.insert(idx, (key, value))
        # 刷盘
        if len(self.memtable) >= self.memtable_limit:
            self.flush_memtable()

    def flush_memtable(self):
        # 刷到SSTable（合并到最前面）
        if self.memtable:
            self.sstables.insert(0, self.memtable)
            self.memtable = []

    def search(self, key):
        # 先查memtable
        idx = bisect.bisect_left([k for k, _ in self.memtable], key)
        if idx < len(self.memtable) and self.memtable[idx][0] == key:
            return self.memtable[idx][1]
        # 再查每个sstable
        for sstable in self.sstables:
            idx = bisect.bisect_left([k for k, _ in sstable], key)
            if idx < len(sstable) and sstable[idx][0] == key:
                return sstable[idx][1]
        return None

    def range_query(self, low, high):
        # 合并memtable和所有sstable的区间结果
        result = []
        def collect(table):
            for k, v in table:
                if low <= k <= high:
                    result.append((k, v))
        collect(self.memtable)
        for sstable in self.sstables:
            collect(sstable)
        # 按key排序去重（最新的覆盖旧的）
        result.sort()
        dedup = {}
        for k, v in result:
            dedup[k] = v
        return [(k, dedup[k]) for k in sorted(dedup) if low <= k <= high]
