# Minesweeper API

REST api for playing classic minesweeper game, with authentication using JWT and game persistence (Postgres DB).
The API had been made public on a free Heroku dyno (https://minesweeper-api-cristian.herokuapp.com)
As it was requested, an API client had been provided in oder to play/interact with this API,
this is also published on Heroku (https://api-client-cristian.herokuapp.com/). This is a simple API Client that does not 
cover all the API functionality but provides a brief view of it.

## API documentation

A full API documentation had been provided using Swagger. This could be accessed from [here](https://minesweeper-api-cristian.herokuapp.com/swagger/)
or it also could be seen using the source found on https://minesweeper-api-cristian.herokuapp.com/static/swagger.json 
and copy and pasting the content on Swagger online editor (https://editor.swagger.io)

## API Instruction 

There are some little things to take in account for playing the game:
- First the user must register it self and the authenticate in order to obtain proper JWT (header would be {Authentication: JWT <access_toke>})
- The user needs to create a new board to play providing the number of rows, columns and mines that s/he prefers
- In order to play the user has 3 options to play:
    - X: to reveal a cell
    - F: to flag a cell
    - ?: in order to mark the cell
- Bombs appears as # , and if a bomb was previously flaged (F) it will appear as #!

## UI Instruction

As it was developed only for a quick look, the [UI App](https://api-client-cristian.herokuapp.com/) has lot of bugs an issue.
So for a proper use these following steps should be followed:
- [Register](https://api-client-cristian.herokuapp.com/register)
- [Login](https://api-client-cristian.herokuapp.com/login)
- [Game List](https://api-client-cristian.herokuapp.com/game)

And from there the user is able to play, pause and resume all the games. 

## Decisions taken

- In order to build the REST API Flask-RESTful was the chosen tool because of its simplicity and easy configuration (time was a main variable to take in acount).
- To manage database scripts and model changes it was used Flask-Migrate, because it simplify all the sql scripting and allow a better control of DB changes.   
- For authentication Flask-JWT was used because web tokens were the best option for this case. 
- I chose PostgreSQL as a DB engine because its flexibility on typing and that allowed me to represent in a confortable way the game characteristics (saving me lot of time).

## Notes
- The API Client only response at a happy game path. It does not support all the validations and erros messages that the API supports. The only excuses for this was the lack of time