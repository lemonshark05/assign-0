# Assignment 0

See Canvas for due date.

The goal is to read in a program in LIR format (as described in the accompanying
file `lir-description.md`) from a file and store it in a data structure that
allows you to easily iterate over functions, basic blocks, and
instructions. This is something that you will need to do for all the upcoming
assignments in this class. The LIR format is intended to be very easy to parse;
the only context-free part is types (see the grammar in `lir-description.md`)
and those are still designed to be trivial to parse.

Optionally, if it's easier for you, the LIR programs are also provided in JSON
format. These are the exact same programs, just pre-parsed and then serialized
as JSON objects. You can choose to __either__ parse the LIR format __or__ read
in the JSON format; you __don't__ need to do both.

A set of LIR programs is contained in the accompanying file `tests.zip`. To help
determine whether you read in the program correctly, for each program file
`<name>.lir` there is a associated file `<name>.stats` that prints out a set of
statistics---you can compute the same statistics from your own data structure
and compare to make sure they are the same. To be clear, the statistics don't
matter themselves, they are just a way to help you determine if you can read in
and iterate over programs correctly.

The statistics are:

- Number of fields across all struct types
- Number of functions that return a value
- Number of function parameters
- Number of local variables
- Number of basic blocks
- Number of instructions
- Number of terminals
- Number of locals and globals with int type
- Number of locals and globals with struct type
- Number of locals and globals with pointer to int type
- Number of locals and globals with pointer to struct type
- Number of locals and globals with pointer to function type
- Number of locals and globals with pointer to pointer type

## Testing your solution

For any test named `tests/foo.lir`, you can run your solution like:

```
./run-stats.sh tests/foo.lir tests/foo.lir.json
```

And, it should print the exact same output as the corresponding `.stats` file.
You can compare the outputs using the `diff` command.  For example:

```
./run-stats.sh tests/foo.lir tests/foo.lir.json > my-stats

./run-stats.sh lecture-2/1.lir lecture.2/1.lir.json

diff -wp my-stats tests/foo.stats
```

I encourage you to build a test runner that runs diff on all tests.

## Reference solutions

I will place executables of my own solutions on vlabs in `~memre/686`.
You can use these reference solutions to test your analyses before
submitting. If you have any questions about the output format, you can answer
them using these reference solutions as well; these are the solutions that
Gradescope will use to test your submissions. My solutions only take two
arguments (as opposed to the three that your solutions should take, described
below): the file containing the LIR program and the name of the function to
analyze.

I will place the solution to this assignment on Friday.

## Submitting to Gradescope

Your submission must meet the following requirements:

- There must be a `build.sh` bash script that does whatever is needed to build
  or setup both analyses (e.g., compile the code if necessary). If nothing is
  necessary the script must still exist, it can just to nothing.

- There must be a `run-stats.sh` bash scripts that each take three command-line
  arguments: the first is a file containing the LIR program to analyze, the
  second is a file containing the same program in JSON format, and the third is
  the name of the function to analyze. You can use whichever program format you
  wish and ignore the other.  Each script must print the result of the respective
  analysis to standard out.

- If your solution contains sub-directories then the entire submission must be
  given as a zip file (this is required by Gradescope for submissions that
  contain a directory structure). The scripts should all be at the root
  directory of the solution.

- The submitted files are not allowed to contain any binaries, and your
  solutions are not allowed to use the network.

I will release the autograder by Friday. Until then, you can test your
solution on the tests your are given.

## Grading

This assignment is graded out of 1 point.  If your solution prints the correct
results for > half of the tests, you get the point.  However, you should make
sure to pass all 100% of the tests, just to guarantee that you can read LIR
files. That's a prerequisite for future assignments.

Here's how the grading will be broken down so that you can focus your work
accordingly. There are two parts to the assignment (constants analysis and
interval analysis), each worth 50 points. For each part, the point breakdown
will be:

- Programs with no pointers or function calls: 25

- Programs with no pointers but with function calls: 5

- Programs with pointers but no function calls: 10

- Programs with pointers and function calls: 10

Remember that you can also create your own test programs and use my solution on
vlabs to see what my solution for that program would be.
