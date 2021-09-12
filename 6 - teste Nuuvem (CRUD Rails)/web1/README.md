# Test Web 1

## Stack used:
- Ruby 2.7.1p83 (2020-03-31 revision a0c7c23c9c) x86_64-linux
- Rails 6.1.4
- SQlite3 3.31.1 
- NodeJS v14.17.4
- Yarn 1.22.5

## Setup:
- Make sure you have the [stack](#stack-used) installed. You can follow the official [Getting Started with Rails](https://guides.rubyonrails.org/getting_started.html#creating-a-new-rails-project-installing-rails) installation guidefui no celu.
- Once everything is installed, inside `/web1` start the server by running `bin/rails server` in your terminal of choice.

## Usability & Instructions:

You should be able to access the project navigating to `http://localhost:3000/`.

`/` (main page) (get):
- Allows the upload of the TAB-separated files.

`/result` (result page) (post):
- Shows the current uploaded file gross income, as well as the all-time gross income.
