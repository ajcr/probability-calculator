# ccc

Command line Combinatorial Calculator for Counting Constrained Collections.

## Introduction

ccc is a calculator that can:

- tell you the *probability* of possible ways a certain collection of items can meet one or more constraints
- *count* the number of possible ways a certain collection of items can meet one or more constraints

For example, consider the following problem (asked on [stats.stackexchange.com](https://stats.stackexchange.com/questions/24211)):

> There are **232** tickets for an event. 363 people apply for a ticket, **12** of whom are from a particular group (so **351** are not from the group). Each ticket is allocated to one person at random and each person can recieve at most one ticket. What is the probability that **at most 2** tickets are given to people in the group?

ccc makes it easy to translate the problem into a single command, handling the tedious computational details from you:

```
$ ccc probability draw --from 'group=12; rest=351' \
                       --number 232 \
                       --constraints 'town <= 2' \
                       --float
0.00093
```

That's roughly 1 in 10000.

Or suppose we're designing a *Magic: The Gathering* deck:

> A deck of 60 cards contains **13** mountain cards and **12** swamp cards. What is the probability that we draw **7** cards and get **between 1 and 3 mountains** and **exactly 2 swamps**?

Using ccc, we can write these constraints very easily:

```
$ ccc prob draw --from 'mountain=13; swamp=12; rest=35' \
                --number 7 \
                --constraints '1 <= mountain <= 3, swamp == 2' \
                --float
0.23264
```

About 23%.

These types of problem are common in everyday life but, depending on how familiar you are with statistics or combinatorics, they can be hard to calculate or even estimate accurately.

See below for numerous other examples and explanations.

## Install

Installation requires Python 3.6 or newer.

```
pip install ccc-calculator
```

## Development install

Clone the repo, create a virtual environment, install the development dependencies, install the module in editable mode, install pre-commit hooks:

```
git clone https://github.com/ajcr/ccc
cd ccc
python -m venv venv
. venv/bin/activate
python -m pip requirements-dev.txt
python -m pip install -e .
pre-commit install
```

Unit tests can be run with `pytest`. Pre-commit hooks will run on each git commit. The hooks can also be invoked with `pre-commit run -a`.

## More examples

The easiest way to introduce ccc is to show various example calculations from the command-line.

ccc is always invoked in the following way:

```
ccc [computation-type] [collection-type] [--args]
```

In all of the examples below, notice how easy it is to express constraints that would otherwise necessitate writing complicated code, or performing repetitive arithmetic on paper.

### Draws

ccc can tell you the probability of selecting particular counts of items from a collection (either with or without replacement).

Here is an example:

> A bag contains:
>
> - 3 red marbles (:red_circle::red_circle::red_circle:)
> - 5 black marbles (:black_circle::black_circle::black_circle::black_circle::black_circle:)
> - 7 blue marbles (:large_blue_circle::large_blue_circle::large_blue_circle::large_blue_circle::large_blue_circle::large_blue_circle::large_blue_circle:)
>
> You must draw at random (and without replacement) 4 of these marbles. You lose if you draw 1 or more of the blue marbles (:blue_circle:).
>
> What is your probability of winning?

To solve this with ccc we can easily specify the *collection* we draw from, the *size* of the draw we make, and any *constraints* on the draw:

```
ccc probability draw --from "red=3; black=5; blue=5" \
                     --number 4 \
                     --constraints "blue == 0"
```
This puts the probability of winning (not drawing a blue marble) at **2/39**, so perhaps we'd win once every 19 or so attempts.

Notice how easy it is to specify the constraints. Just the item's name (*blue*) and its desired count (*0*). Any comparison operators can be used (`==`, `!=`, `<`, `<=`, `>`, `>=`).

If we wanted to allow a marble to be replaced after each draw, we would add the `--replace` flag.

---

We can specify more complicated constraints on what we want to draw from the bag:

> This time, draw **5** marbles without replacement from the same collection, but with 2 white marbles (:white_circle::white_circle:)  added.
>
> You win a toy if you draw a collection which comprises
>
> - both white marbles (:white_circle::white_circle:), **and**
> - at least 1 black marble (:black_circle:**+**)
>
> What is you chance of winning the toy?

```
ccc probability draw --from "red=3; black=5; blue=7; white=2" \
                     --number 5 \
                     --constraints "white == 2, black >= 1"
```
Our chance of winning is **3/119** according to ccc, so we would expect to win around once every 40 attempts.

You can see that to express multiple constraints on our draw, we simply used commas `,` to separate them.

---

Lastly, it is possible to use `or` (any number of times) in constraints:

> Draw **3** marbles such that you get:
>
> - 3 red marbles (:red_circle::red_circle::red_circle:) **or**
> - 1 white, 1 black and 1 blue marble (:white_circle::black_circle::large_blue_circle:)
>
> What is the probability of succeeding now?

```
ccc probability draw --from "red=3; black=5; blue=7; white=2" \
                     --number 3 \
                     --constraints "red == 3 or (white == 1, black == 1, blue == 1)"
```
The probability is **0.1**.


### Multisets

Multisets are unordered collections (like sets) in which an item may appear multiple times.

> How many ways can we gather up 20 pieces of fruit such that we have:
>
> - fewer than 10 apples (:green_apple:), **and**
> - at least 5 bananas (:banana:), **and**
> - the number of grapes is not 13 (:grapes:), **and**
> - there are are even number of strawberries (:strawberry:)?

```
ccc count multisets --size 20 \
                    --constraints 'apples < 10, bananas >= 5, grapes != 13, strawberries % 2 == 0'
```

The answer is **406**.

The modulo (`%`) operator used above provides the facility to solve coin change problems, for example:

> The UK currency has the following coins:
>
>   1p, 2p, 5p, 10p, 20p, 50p, £1 (100p) and £2 (200p)
>
> How many different ways can £5 be made using any number of coins?
>
> cf. [Project Euler problem 31](https://projecteuler.net/problem=31)

```
ccc count multisets --constraints 'a%1==0, b%2==0, c%5==0, d%10==0, e%20==0, f%50==0, g%100==0, h%200==0' \
                    --size 500
```

The answer is computed within a couple of seconds as **6,295,434** different ways.

We could also put additional contraints on the coins, such as restricting the number of times a coin may be used.

### Permutations

Permutations of words can be counted as follows:

```
ccc count permutations MISSISSIPPI
```

There are **34650** unique permutations of this famous river/state.

What about if we only count permutations where instances of the same letter are not adjacent to each other?

```
ccc count permutations MISSISSIPPI --constraints no_adjacent
```

Using the 'no_adjacent' constraint, the answer comes back immediately as **2016**. The speed of this calculation is thanks to the use of [Generalised Larguerre Polynomials](https://arxiv.org/pdf/1306.6232.pdf).

We can also treat the letters as distinguishable (the `--same-distinct` flag) to solve a related type of problem:

> Five couples are to seated in a row. How many ways can they be seated such no couples are seated together?

```
ccc count permutations AABBCCDDEE --constraints no_adjacent --same-distinct
```

**1,263,360** ways.

ccc allows derangements (permutations where no item occupies its original place) to be counted.

> Five couples draw names from a hat. What is the probability that nobody draws either their own name, or the name of their partner?

```
ccc probability permutation AABBCCDDEE --constraints derangement --float
```

It turns out that there is only a **0.121** probability of this occurring.

### Sequences

Sequences are ordered collections of items.

> How many 30 letter sequences can you make using no more than 20 each of **A**, **B** and **C**?

```
ccc count sequences --size 30 --constraints 'A <= 20, B <= 20, C <= 20'
```

The answer is a lot: there are **205,863,750,414,990** such sequences.
