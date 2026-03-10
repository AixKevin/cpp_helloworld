#include "Random.h"

#include <iostream>
#include <string>
#include <string_view>

using namespace std::literals;

class Monster
{
public:
    enum Type
    {
        dragon,
        goblin,
        ogre,
        orc,
        skeleton,
        troll,
        vampire,
        zombie,
        maxMonsterTypes,
    };

private:
    Type m_type{};
    std::string m_name{"???"};
    std::string m_howl{"???"};
    int m_health{};

public:
    Monster(Type t, std::string_view n, std::string_view h, int hp) : m_type{t}, m_name{n}, m_howl{h}, m_health{hp} {}
    const std::string_view getTypeString() const
    {
        switch (m_type)
        {
        case dragon:
            return "dragon"sv;
        case goblin:
            return "goblin"sv;
        case ogre:
            return "ogre"sv;
        case orc:
            return "orc"sv;
        case skeleton:
            return "skeleton"sv;
        case troll:
            return "troll"sv;
        case vampire:
            return "vampire"sv;
        case zombie:
            return "zombie"sv;
        default:
            return "???";
        }
    }
    void print() const
    {
        if (m_health <= 0)
        {
            std::cout << m_name << " the " << getTypeString() << " is dead.\n";
        }
        else
        {
            std::cout << m_name << " the " << getTypeString() << " has " << m_health << " hit points and says " << m_howl << ".\n";
        }
    }
};

namespace MonsterGenerator
{
    std::string_view getName(int n)
    {
        switch (n)
        {
        case 0:
            return "Blarg";
        case 1:
            return "Moog";
        case 2:
            return "Pksh";
        case 3:
            return "Tyrn";
        case 4:
            return "Mort";
        case 5:
            return "Hans";
        default:
            return "???";
        }
    }
    std::string_view getRoar(int n)
    {
        switch (n)
        {
        case 0:
            return "*ROAR*";
        case 1:
            return "*peep*";
        case 2:
            return "*squeal*";
        case 3:
            return "*whine*";
        case 4:
            return "*growl*";
        case 5:
            return "*burp*";
        default:
            return "???";
        }
    }
    Monster generate()
    {
        return Monster{static_cast<Monster::Type>(Random::get(0, 7)), getName(Random::get(0, 5)), getRoar(Random::get(0, 5)), Random::get(0, 100)};
    }
} // namespace MonsterGenerator

int main()
{
    Monster m{MonsterGenerator::generate()};
    m.print();

    return 0;
}
