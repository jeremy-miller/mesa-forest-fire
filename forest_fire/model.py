import mesa

from forest_fire.tree import Tree


class ForestFire(mesa.Model):
    def __init__(
        self,
        width=100,
        height=100,
        tree_density=0.65,
        tree_ignition_rate=0.1,
        tree_regrowth_rate=0.25,
    ):
        super().__init__()
        self.width = width
        self.height = height
        self.tree_density = tree_density
        self.tree_ignition_rate = tree_ignition_rate
        self.tree_regrowth_rate = tree_regrowth_rate
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.SingleGrid(self.width, self.height, torus=False)

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Fine": lambda model: self.count_type(model, "Fine"),
                "On Fire": lambda model: self.count_type(model, "Burning"),
                "Burned": lambda model: self.count_type(model, "Burned"),
            }
        )

        self._initialize_trees()

        self.datacollector.collect(self)

    def _initialize_trees(self):
        for _contents, pos in self.grid.coord_iter():
            if self.random.random() < self.tree_density:
                tree = Tree(self.next_id(), self, pos)
                if pos[0] == 0:
                    tree.status = "Burning"
                self.schedule.add(tree)
                self.grid.place_agent(tree, pos)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    @staticmethod
    def count_type(model, status):
        count = 0
        for tree in model.schedule.agents:
            if tree.status == status:
                count += 1
        return count