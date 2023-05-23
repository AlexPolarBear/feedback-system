import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from rankingSystem import RankingSystem

if __name__ == "__main__":
    print("[*] Service RankingSystem start work! [*]\n")
    ranking_system = RankingSystem()

    ranking_system.update_courses()
    ranking_system.update_tags()
    ranking_system.update_users()

    req = "Алгебраические кольца"
    tags = ranking_system.get_top_suitable_tags_by_text(req=req)
    print(tags)
    
    tags = ranking_system.get_top_suitable_tags_by_text(req=req, metric_func=RankingSystem._inv_levenshtain_ratio)
    print(tags)