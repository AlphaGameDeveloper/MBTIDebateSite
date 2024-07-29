# MBTIDebateSite API

## API::accessInternals
```
GET /api/accessInternals
```
Access the entire internal `globalData` for the entire application in a JSON format.

```
GET /api/accessInternals/<key>
```
Access a specific key in the application `globalData`.  Examples:

`GET /api/accessInternals/dominant` - Get the dominant cognitive function.

`GET /api/accessInternals/type_main` - Get the MBTI list for the main type, vice versa for `type_shadow`.

## API::reset
```
GET /api/reset
```
Reset the application's `globalData` to the startup default.  Simple as that.

## API::userConfigHandler
```
GET /api/userConfigHandler
```
Takes a query param, `username`, and returns a redirect while also setting the `username` cookie.

## API::submitCurrentState
```
POST /api/submitCurrentstate
```
Takes post data in the form of JSON, and applies it to `globalData.`

Example to set the MBTI to ENTP (`Ne - Ti - Fe - Si`) via cURL

`curl '(address)/api/submitCurrentstate' --data-raw '{"dominant":"ne","auxiliary":"ti","tertiary":"fe","inferior":"si"}'`

## API::getStack
```
GET /api/getStack
```
**WARNING: THIS WILL RETURN HTML, AND IS INTENDED TO BE USED IN THE MAIN APPLICATION, AFTER HTMX IS LOADED.**

Get a HTML table containing all the cognitive functions (including shadow functions) in a HTML table, with HTMX to automatically get new data.

If you want the cognitive function data, or any real data, please use `/api/accessInternals`.

## API::requestCount
```
GET /api/requestCount
```
Get the amount of requests sent to the server.

This was meant to be used in the debug view but was ultimately scrapped.
