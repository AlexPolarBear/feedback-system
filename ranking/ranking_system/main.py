from rankingSystem import RankingSystem



if __name__ == "__main__":
    print("Service RankingSystem start work!")
    ranking_system = RankingSystem()

    ranking_system.update_courses()
    courses = ranking_system._get_courses()
    # print(courses)
    # ranking_system._print_courses()

    ranking_system.update_users()
    users = ranking_system._get_users()
    # print(users)
    
    top_courses = ranking_system.get_top_match_user_and_course(users[0])

    print(top_courses[1])

    