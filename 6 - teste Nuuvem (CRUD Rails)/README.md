# Test Web 1

The idea with this test is to allow us to better comprehend the skills of candidates to developer jobs, in various experience levels.

This test should be completed by you on your own, in your own time. Take as much time as you need, but usually this test shouldn't take more than a few of hours to be done.

## Delivery instructions

Download the instructions and example input file from this repo and, once done, put all project files in a .zip file and send it to your contact at Nuuvem or submit it via the Recruitee link you received, if any.

## Project description

You've received a text file (tab separated) with data describing the company sales. We need a way for this data to be imported to a database to be analyzed later.

Your job is to create a web interface that accepts file uploads, normalizes the data and stores it in a relational database.

Your application MUST:

1. Accept (via HTML form) file uploads of TAB-separated files, with the following columns: `purchaser name`, `item description`, `item price`, `purchase count`, `merchant address`, `merchant name`. You can assume the columns will always be in that order, and that there will always be some value in each column, and that there will always be a header row. An example file called `example_input.tab` is included on this repo.
1. Interpret (parse) the received file, normalize the data, and save the data correctly in a relational database. Don't forget to model the entities imported from the file data, considering their relationships.
1. Show the total gross income represented by the sales data after each file upload, and also the total all-time gross income.
1. Be written in Ruby 2.5 or greater (or, in the language solicited by the job description, if any).
1. Have good automated tests coverage.
1. Be simple to configure and execute, running on a Unix-compatible environment (Linux or macOS).
1. Use only free / open-source language and libraries.

Your application doesn't need to:

1. Deal with authentication or authorization (bonus points if it does, though, specially via oAuth).
1. Be developed with any specific framework (but there's nothing wrong with using them, use what you think is best for the task).
1. Be pretty.

## Review

Your project will be evaluated by the following criteria:

1. Does the application fulfill the basic requirements?
1. Did you document how to configure and run the application?
1. Did you follow closely the project specification?
1. Quality of the code itself, how it's strutured and how it complies with good object-oriented practices;
1. Quality and coverage of unit / funcional / automated tests;
1. Familiarity with the standard libraries of the language and other packages;

### Reference

This test was based on this other test: https://github.com/lschallenges/data-engineering
