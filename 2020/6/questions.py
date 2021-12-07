
import sys

quest_map = dict()
total_questions = 0
with open(sys.argv[1]) as f:
    for line in f:
        if line.rstrip() == "":
            questions_all = 0
            for key in quest_map:
                if key != 'count':
                    if (quest_map[key] == quest_map['count']):
                        questions_all += 1
                        
            total_questions += questions_all
            print("NUM:", questions_all, total_questions)
            quest_map = dict()
        else:
            quest_map['count'] = quest_map.get('count', 0) + 1
            for i in range(len(line.rstrip())):
                quest_map[line[i]] = quest_map.get(line[i], 0) + 1
            print(line.rstrip(), "len", len(quest_map), "voters:", quest_map['count'])

print("answer p2", total_questions)