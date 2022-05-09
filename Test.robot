*** Settings ***
Library    SeleniumLibrary


*** Test Cases ***

QA

    open browser    http://www.google.com   firefox
    maximize browser window
    close all browsers
