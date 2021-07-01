class PIT():
    def __init__(self):
        self.route_ID = 0
        self.pit = {}

    def Create_pit(self, route_ID):
        self.route_ID = route_ID

    def Get_pit(self):
        return self.pit

    def Get_pit_entry(self, content_name):
        return pit.get(content_name)

    def Update_pit_outface(self, pit, Outfaces, interest):
        content_name = interest['content_name']
        for i in Outfaces:
            if i in self.pit[content_name][1]:
                continue
            else:
                self.pit[content_name][1].append(i)

    def Merge_pit_entry(self, interest):
        content_name = interest['content_name']
        route_ID = interest['route_ID']
        if route_ID in self.pit[content_name][0]:
            return
        else:
            self.pit[content_name][0].append(route_ID)

    def Create_pit_entry(self, interest):
        content_name = interest['content_name']
        route_ID = interest['route_ID']
        if content_name in self.pit:
            return
        else:
            self.pit[content_name] = [[route_ID],[]]

    def Search_pit_interest(self, pit, interest):
        content_name = interest['content_name']
        if self.pit.get(content_name) != None:
            self.Merge_pit_entry(interest)
            return False
        else:
            self.Create_pit_entry(interest)
            return True

    def Search_pit_data(self, pit, data):
        if data['content_name'] in pit:
            return True
        else:
            return False

    def Remove_pit_entry(self, pit, data):
        content_name = data['content_name']
        if content_name in pit:
            del self.pit[content_name]

    def print_PIT(self):
        print("r%d " % self.route_ID, self.pit)
