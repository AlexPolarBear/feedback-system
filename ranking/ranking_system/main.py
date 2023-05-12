from rankingSystem import RankingSystem



if __name__ == "__main__":
    print("[*] Service RankingSystem start work! [*]\n")
    ranking_system = RankingSystem()

    ranking_system.update_courses()
    ranking_system.update_tags()
    ranking_system.update_users()

    req = "Алгебраические кольца"
    tags = ranking_system.get_top_nearest_tags(req=req)
    print(tags)
    
    tags = ranking_system.get_top_nearest_tags(req=req, metric_func=RankingSystem._inv_levenshtain_ratio)
    print(tags)