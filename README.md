# HTTP Client


This library provides an Http client for Pyxus with support of OpenID token authentication.

A basic authentication client is provided as well as an abstract class.

## Abstract Auth Client


This class allows the user to implement its own client by defining the required methods.

## Basic Auth Client


This client uses the token provided. Once the token expires no refresh is done.

## OpenID Client


This client allows to either pass a refresh token in its constructor. This token will be refresh when needed. 
If no refresh token are provided, the client will search for a token in the refresh_token_file_path. 
If you do not have any  refresh token you can use the exchange_code_for_token method that will save the refresh_token
in the refresh_token_file_path provided.
