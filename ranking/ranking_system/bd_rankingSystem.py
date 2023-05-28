import requests


class BD_RankingSystem:
    SERVER_IP = "127.0.0.1"
    PORT = 5000
    PROTOCOL = "http"

    @staticmethod
    def _prefix_link():
        res_link = f"{BD_RankingSystem.PROTOCOL}://{BD_RankingSystem.SERVER_IP}:{BD_RankingSystem.PORT}/"
        return res_link
    
    @staticmethod
    def _final_link(*paths : str):
        final_link = BD_RankingSystem._prefix_link()
        for path in paths:
            final_link = f"{final_link}/{path}"
        return final_link
    
    @staticmethod
    def get_all_courses():
        endpoint = "courses"
        res_link = BD_RankingSystem._final_link(endpoint)
        
        # это без тегов
        courses_json =  requests.get(res_link)





if __name__ == "__main__":
    bd_rs = BD_RankingSystem()
    print(bd_rs.get_all_courses())
    


