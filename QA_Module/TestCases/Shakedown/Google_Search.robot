*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${google_url}   http://www.google.com
${browser}  firefox
${search_bar}   xpath=.//*[contains(@name,'q')]

*** Test Cases ***

Open-Google-Firefox

    open browser    ${google_url}   ${browser}
    maximize browser window
    input text    ${search_bar}    test
    log to console    \nentered test
    input text  ${search_bar}   gmail
    close all browsers
