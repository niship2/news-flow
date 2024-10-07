def return_period(nws, time_op):
    if nws == "google":
        if time_op == "直近24時間":
            return "d1"
        elif time_op == "直近1週間":
            return "w1"
        elif time_op == "直近2週間":
            return "w2"
        elif time_op == "直近1ヶ月":
            return "m1"
        elif time_op == "過去1年":
            return "1y"
        else:
            return "d1"
    elif nws == "bing":
        if time_op == "直近24時間":
            return "Day"
        elif time_op == "直近1週間":
            return "Week"
        elif time_op == "直近2週間":
            return "Week"
        elif time_op == "直近1ヶ月":
            return "Month"
        elif time_op == "過去1年":
            return "Month"      
        else:
            return "Day"
    elif nws == "youcom":
        if time_op == "直近24時間":
            return "day"
        elif time_op == "直近1週間":
            return "week"
        elif time_op == "直近2週間":
            return "week"
        elif time_op == "直近1ヶ月":
            return "month"
        elif time_op == "過去1年":
            return "year"        
        else:
            return "day"
    else:
        return "m1"