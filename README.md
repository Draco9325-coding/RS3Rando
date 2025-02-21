# RS3Rando v0.4.0

RS3Rando is a (Currently WIP) randomizer for the Super Famicom title "Romancing SaGa 3."

## Features the following

* Shuffle or Randomize personal stats

Randomizing stats supports a minimum stat value, a maximum, a BST to aim for, and a variance from the BST the randomizer is allowed to stray off.

* Randomize Weapon Level Growths

Randomize the rate a character's weapon type proficiency will grow.

* Shuffle or Randomize Weapon Level bases

Change the weapon type proficiencies a character starts with, either by shuffling their vanilla values around, or by completely randomizing them into something new

* Star Sign, Favorite Weapon, Spark type, and modifier Randomization

Change what spark type, favorite weapon, and/or star sign a character has, leading to altered stats.
You can also change how large the applied modifiers are, but things might get very broken if you're not careful

* ROM copy and Changelog!

Writes the changed stats to a separate ROM file of the user's choosing and to a .txt changelog next to the output ROM. Yay for preserving the original ROM file!

### More to be added in later versions!

## TODO

Add support for more options, such as:

* Technique Discount Bonus
* Chest Randomization
* Weapon/Armor stat randomization
* Possibly more, depending on my understanding of Romancing SaGa 3


## Important Notes

* Mana Sword's EN and Magno's ES translations vs JP

Comparing the differences between Magno's TL and the JP ROM, there appears to
be little, if any, difference in where the data that is modified is stored. This
makes the Spanish fantranslation readily compatible with the randomizer.

For Mana Sword's EN translation, it is necessary to use a version of the ROM with a
200-byte empty header to even get the translation hack working, otherwise attempts to load the game, even when not randomized,
will fail. 

I have added a method to check for this discrepency in
data, thus having support for Mana Sword's EN patch.

