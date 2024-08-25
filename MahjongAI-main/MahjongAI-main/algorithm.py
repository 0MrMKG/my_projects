import re
global count_9z

def modify_to_multiple_of_three(num):
    remainder = num % 3
    return num - remainder if remainder <= 1 else num + 3 - remainder

def get_handcards(string):
    fullmatch = re.fullmatch(r'(\d+[mps]|[1-7]+z)+', string)
    if not fullmatch:
        print('Invalid Input')
        return
    match = re.findall(r'\d+[mps]|[1-7]+z', string)
    carddict = {
        'm': [], 'p': [], 's': [], 'z': []
    }
    for cards in match:
        type_ = cards[-1]
        for i in cards[:-1]:
            if i == '0': #红宝牌
                carddict[type_].append(5)
            else:
                carddict[type_].append(int(i))
        carddict[type_].sort()
    num = sum(len(carddict[tp]) for tp in 'mpsz')
    if num not in [14, 11, 8, 5, 2]:
        print('Wrong number of cards')
        return
    if num in [11, 8, 5, 2]:
        carddict['z'] += [9] * (14 - num)
    return carddict

'''
carddict = {
        'm':[], 'p':[], 's':[], 'z':[]
    }
'''

class HandCards:
    def __init__(self, carddict):
        self.carddict = carddict
        self.num = sum(len(carddict[tp]) for tp in 'mpsz')

    def taatsucount(self):
        toitsu, taatsu, mentsu = (0, 0, 0)
        carddict_cpy = {
            'm': self.carddict['m'][:],
            'p': self.carddict['p'][:],
            's': self.carddict['s'][:],
            'z': self.carddict['z'][:]
        }

        # 先处理刻子
        for tp in 'mpsz':
            i = 1
            while i < len(carddict_cpy[tp]):
                if carddict_cpy[tp].count(carddict_cpy[tp][i]) >= 3:
                    target = carddict_cpy[tp][i]
                    for _ in range(3):
                        carddict_cpy[tp].remove(target)
                    mentsu += 1
                else:
                    i += 1

        # 处理顺子
        for tp in 'mps':
            for i in range(1, 8):
                if i in carddict_cpy[tp] and i + 1 in carddict_cpy[tp] and i + 2 in carddict_cpy[tp]:
                    carddict_cpy[tp].remove(i)
                    carddict_cpy[tp].remove(i + 1)
                    carddict_cpy[tp].remove(i + 2)
                    mentsu += 1

        # 处理对子
        for tp in 'mps':
            i = 1
            while i < len(carddict_cpy[tp]):
                if carddict_cpy[tp].count(carddict_cpy[tp][i]) == 2:
                    target = carddict_cpy[tp][i]
                    for _ in range(2):
                        carddict_cpy[tp].remove(target)
                    toitsu += 1
                else:
                    i += 1

        # 处理搭子
        for tp in 'mps':
            for i in range(1, 9):
                if i in carddict_cpy[tp]:
                    if i + 1 in carddict_cpy[tp]:
                        carddict_cpy[tp].remove(i)
                        carddict_cpy[tp].remove(i + 1)
                        taatsu += 1
                    elif i + 2 in carddict_cpy[tp]:
                        carddict_cpy[tp].remove(i)
                        carddict_cpy[tp].remove(i + 2)
                        taatsu += 1

        # 剩余手牌检验
        if mentsu + toitsu + taatsu + sum(len(carddict_cpy[tp]) for tp in 'mpsz') < (
                sum(len(carddict_cpy[tp]) for tp in 'mpsz') + 1) // 3:
            taatsu -= 1

        return (toitsu, taatsu, mentsu)

    def shanten(self):
        #国！
        st_kokushi = 13
        if self.num == 14:
            carddict_cpy = {
                'm':self.carddict['m'].copy(),
                'p':self.carddict['p'].copy(),
                's':self.carddict['s'].copy(),
                'z':self.carddict['z'].copy()
            }
            for tp in 'mps':
                if 1 in carddict_cpy[tp]:
                    st_kokushi -= 1
                    carddict_cpy[tp].remove(1)
                if 9 in carddict_cpy[tp]:
                    st_kokushi -= 1
                    carddict_cpy[tp].remove(9)
            for i in range(1,8):
                if i in carddict_cpy['z']:
                    st_kokushi -= 1
                    carddict_cpy['z'].remove(i)
            if carddict_cpy['z']:
                st_kokushi -= 1
            else:
                for tp in 'mps':
                    if 1 in carddict_cpy[tp] or 9 in carddict_cpy[tp]:
                        st_kokushi -= 1
                        break

        #七对
        toitsu = 0
        dragon = 0 #
        if self.num == 14:
            for tp in 'mpsz':
                for i in range(1,10):
                    if i in self.carddict[tp] and self.carddict[tp].count(i) == 4:
                        dragon += 1
                    elif i in self.carddict[tp] and self.carddict[tp].count(i) >= 2:
                        toitsu += 1
        if toitsu + 2 * dragon == 7:
            st_chitoi = 2 * dragon - 1
        else:
            st_chitoi = 6 - toitsu - dragon


        #一般情况
        tuple_ = self.taatsucount()
        block = sum(tuple_)
        toitsu, taatsu, mentsu = tuple_

        count_9z = self.carddict['z'].count(9)
        #print(int(modify_to_multiple_of_three(count_9z)/3))#相当于这里多记录了这么多组9z的刻字，但似乎没有用了
        #st_ippan -= int(modify_to_multiple_of_three(count_9z)/3)
        #print(int(modify_to_multiple_of_three(count_9z)/3))

        if toitsu == 0:
            st_ippan = 8 - 2 * mentsu - taatsu + max(0, block - 4)
        else:
            st_ippan = 8 - 2 * mentsu - taatsu - toitsu + max(0, block - 5)

        return min(st_kokushi, st_chitoi, st_ippan)

    def jinzhang(self, card_num, card_tp):
        ret_str = ''
        num = 0
        carddict_cpy = {
            'm': self.carddict['m'][:],
            'p': self.carddict['p'][:],
            's': self.carddict['s'][:],
            'z': self.carddict['z'][:]
        }
        handcards_cpy = HandCards(carddict_cpy)
        for tp in 'mpsz':
            handcards_cpy.carddict[card_tp].remove(card_num)
            for i in range(1, 10):
                if tp == 'z' and i > 7:
                    break
                if self.carddict[tp].count(i) == 4:
                    continue
                handcards_cpy.carddict[tp].append(i)
                handcards_cpy.carddict[tp].sort()
                if handcards_cpy.shanten() < self.shanten():
                    ret_str += str(i) + tp
                    num += 4 - self.carddict[tp].count(i)
                handcards_cpy.carddict[tp].remove(i)
            handcards_cpy.carddict[card_tp].append(card_num)
        return (ret_str, num)

    def print_jinzhang(self) ->str:
        strlist = []
        choice_cards_can_be_made = []
        for tp in 'mpsz':
            for card_num in set(self.carddict[tp]):
                drawcard, num = self.jinzhang(card_num, tp)
                if num > 0:
                    discard = str(card_num) + tp
                    strlist.append((discard, drawcard, num))
        strlist.sort(key=lambda tuple_: (tuple_[0][1], tuple_[0][0]))
        strlist.sort(key=lambda tuple_: tuple_[2], reverse=True)
        if self.num == 14:
            for tuple_ in strlist:
                if tuple_[0] == '9z':
                    continue
                str_ = '打' + tuple_[0] + ' 摸{} 共{}枚'.format(tuple_[1], tuple_[2])
                print(str_)
                choice_cards_can_be_made.append((tuple_[0],tuple_[2]))
            print(choice_cards_can_be_made)
            sorted_data = sorted(choice_cards_can_be_made, key=lambda x: (-x[1], int(x[0][-1] != 'z'), -abs(int(x[0][:-1]) - 5), -int(x[0][:-1])))
            result = sorted_data[0][0]
            return result


def card_matching_algorithm(string):
    global handcards, result
    if len(string) == 3 and string[0] == string[1]:
        print('Ron!')
        return
    if string[0].isalpha():
        string = string[1:]
    string = list(string)
    i = 1
    while i < len(string):
        if string[i].isalpha() and string[i-1].isalpha():
            string.pop(i)
        else:
            i += 1
    string = ''.join(string) #防止缺某种牌
    try:
        if get_handcards(string):
            handcards = HandCards(get_handcards(string))
            if handcards.shanten() < 0:
                print('Ron!')
            elif handcards.shanten() == 0:
                print('聴牌!')
                result = handcards.print_jinzhang()
            else:
                print('{}向听.'.format(handcards.shanten()))
                result = handcards.print_jinzhang()
                #print(result)
                return result
    except Exception as e:
        print('An error occurred:', e)



if __name__ == "__main__":
    card_matching_algorithm('556m3458p5789s777z')