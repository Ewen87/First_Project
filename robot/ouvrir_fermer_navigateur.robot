*** Settings ***
Library    SeleniumLibrary


*** Variables ***
${url}    http://example.com

*** Test Cases ***
Ouvrir et Fermer Navigateur

    [Documentation]    Ouvrir le navigateur et aller à l'URL spécifiée, puis fermer le navigateur.
    Open Browser    ${url}    chrome
    Sleep    5 seconds
    Close Browser