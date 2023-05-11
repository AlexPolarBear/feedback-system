from rankingSystem import RankingSystem



if __name__ == "__main__":
    print("Service RankingSystem start work!")
    ranking_system = RankingSystem()

    ranking_system.update_courses()

    ranking_system._print_courses()