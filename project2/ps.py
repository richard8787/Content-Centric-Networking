class PS():
    def __init__(self):
        self.ps = []
        self.ps_route_ID = -1
        self.ps_content_num = -1

    def Create_ps(self, route_ID, content_num, producer_content):
        self.ps_route_ID = route_ID
        self.ps_content_num = content_num
        self.ps = producer_content

    def Get_ps(self):
        return self.ps

    def Search_ps_interest(self, ps, content_name):
        if content_name in ps:
            return True
        else:
            return False
