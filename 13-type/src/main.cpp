#include <iostream>
#include <string>
#include <string_view>

struct Monster
{
    enum Type
    {
        ogre,
        dragon,
        animalman,
        giant_spider,
        slime
    } type{};
    std::string name;
    int health;
};

constexpr std::string_view getMonsterType(Monster::Type mt)
{
    switch (mt)
    {
    case Monster::ogre:
        return "Ogre";
    case Monster::dragon:
        return "Dragon";
    case Monster::animalman:
        return "Animalman";
    case Monster::giant_spider:
        return "Giant Spider";
    case Monster::slime:
        return "Slime";
    default:
        return "???";
    }
}

std::ostream &operator<<(std::ostream &out, Monster::Type mt)
{
    out << getMonsterType(mt);
    return out;
}

const void printMonster(const Monster &monster)
{
    std::cout << "This " << monster.type << " is named " << monster.name << " and has " << monster.health << " health.\n";
}

int main()
{
    const Monster ogre_1{Monster::ogre, "Ogre", 145};
    printMonster(ogre_1);
    const Monster slime_1{Monster::slime, "Blurp", 23};
    printMonster(slime_1);
    return 0;
}
