# -*- coding: utf-8 -*-
import requests
import json
import datetime
import os
import configparser

def getToday():
  today = datetime.date.today()
  return today

def getTodayDir(today):
  todayDirPath = '/{}/'.format(str(today))
  return todayDirPath

def main():
  config = configparser.ConfigParser()
  config.sections()
  config.read('credentials.ini')

  user = config['DEFAULT']['user']
  password = config['DEFAULT']['password']
  httpUrl = config['DEFAULT']['url']

  # write - übersicht alle 14 Filialen
  r_livePointsOfSales = requests.get(httpUrl, auth=(user, password))

  # liste von verfügbaren filialen
  avaliableStoresNr = []
  jsonObjList = []
  storesHRef = {}

  # fügt alle verfügbaren filialen hinzu
  for index in range(0, len(r_livePointsOfSales.json())):
    avaliableStoresNr.append(r_livePointsOfSales.json()[index]['PosNumber'])

  # speichert das json der filiale falls verfügbar
  for jsonObj in r_livePointsOfSales.json():
    if jsonObj['PosNumber'] in avaliableStoresNr:
      jsonObjList.append(jsonObj)

  # erzeugt eine dict mit key: PosNumber, value: HRef
  for obj in jsonObjList:
    url = obj['Links'][0]['HRef']
    posNr = obj['PosNumber']
    storesHRef.setdefault(posNr, []).append(url)

  # speichert alle filialen ab
  for url in storesHRef:
    httpLink = storesHRef[url][0]
    temp_filialeSales = requests.get(httpLink, auth=(user, password))
    todayDirPath = getTodayDir(getToday())
    filePathName = todayDirPath + str(url) + '_' + str(getToday()) + '.json'
    if not os.path.exists(todayDirPath):
        os.makedirs(todayDirPath)
    with open (filePathName, 'w') as outfile:
      json.dump(temp_filialeSales.json(), outfile)
      print('saved' + filePathName)

if __name__ == "__main__":
  main()
