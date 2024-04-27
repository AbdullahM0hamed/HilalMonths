# What is this

A sighting-based collection of the 1st day of hijri months from sighting organisations around the world. The data gathered here will be from varying organisations around the world. These organisations will have different methodologies they follow such as global vs local sighting. I also do not vouch for the integrity of any of the sightings, but only that I will faithfully gather the data from the organisations.

# Usage

The data can be gotten from here [here](https://raw.githubusercontent.com/AbdullahM0hamed/HilalMonths/master/hilal-months.json). The data is organised as follows:

1 - There is a list of groups which contains a list of all the group names. The group names can then be used as a key to get that group's sighting information. I may introduce a v2 of the sighting and remove this due to the redundancy of this list as you can simply get the keys.

2 - Each group will have key pairs with the key being a hijri year (starting from the latest year) and a value that is a json.

3 - The json value of a given hijri year contains key-value pairs of a month (represented as a number from 1 - 12, starting from Muḥarram) and the first day of that month in the gregorian calendar (dd/mm/yyyy or dd/m/yyyy if month is a single digit). The gregorian date corresponds to the hijri date that overlaps it from midnight to sunset, and which will have started the sunset prior in the previous gregorian day.

Currently this data does not include whether or not the sighting report for a given month was positive or negative, this maybe a considered in the future.

# Projects that use this

This is used by the following projects:

- [HijriDate](https://hijridate.github.io)

- [HilalWidget](https://github.com/AbdullahM0hamed/HilalWidget)
