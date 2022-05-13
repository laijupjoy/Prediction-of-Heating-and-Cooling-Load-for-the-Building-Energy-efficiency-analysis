#Database Name : energyefficiency
#Keyspace Name : energy
#Table Name : energy_data

from application_logging.logger import App_Logger
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pandas as pd
import csv

logger = App_Logger('logFiles/database.log')


class dataBaseOperation:

    def __init__(self):

        logger.info('INFO', 'Trying To Connect With The DataStax Server')
        self.keyspace = "energy"

        self.table_name = "energy_data"

        self.client_id = 'teTkOUrOjCRLvXzlclASDKLW'

        self.client_secret = 'UCs12v.D8_ziNanMzYnTMfylI9Qj13e1gyrbMDk.c+u69um59jENIjujnB.DN2K+2MnamT.TvYLtO,nk7.qe-w07NboIpwBxBjID0Dwrds7jXwfoOuej.sEDibgems5f'

        self.cloud_config = {
            'secure_connect_bundle': r"C:\Users\Lenovo\PycharmProjects\EnergyEfficiency\secure-connect-energyefficiency.zip"}

        auth_provider = PlainTextAuthProvider(self.client_id, self.client_secret)
        cluster = Cluster(cloud=self.cloud_config, auth_provider=auth_provider)
        self.session = cluster.connect()
        # print('Connection Is Created')
        logger.info('INFO', 'Connetion Is Created With DataStax Server')

    def useKeySpace(self):

        try:

            logger.info('INFO', 'Using The Keyspace That We Created At Time of Database Creating')
            self.session.execute("USE {keyspace};".format(keyspace=self.keyspace))
            # print('Using The energy Keyspace')
            logger.info('INFO', 'The {keyspace} Is Selected'.format(keyspace=self.keyspace))

        except Exception as e:
            raise Exception(f"(useKeySpace) - Their Is Something Wrong About useKeySpace Method \n" + str(e))

    def createTable(self):

        try:

            logger.info('INFO', 'Table Is Creating Inside The Selected Keyspace')
            self.session.execute("USE {keyspace};".format(keyspace=self.keyspace))
            self.session.execute(
                "CREATE TABLE {table_name}(ID int PRIMARY KEY,X1 float,X2 float,X3 float,X4 float,X5 float,X6 int,X7 float,X8 int,Y1 float, Y2 float);".format(table_name=self.table_name))
            # print('Table Is Created Inside The Keyspace')
            logger.info('INFO', 'The Table Is Created Inside The {keyspace} With Name {table_name}'.format(keyspace=self.keyspace, table_name=self.table_name))

        except Exception as e:
            raise Exception(f"(createTable) - Their Is Something Wrong About Creating Table Method \n" + str(e))

    def insertIntoTable(self):

        try:

            logger.info('INFO', 'Trying To Add Data Into The Database')
            data = pd.read_csv(r"Dataset/ENB2012_data.csv", sep=',', index_col='ID')
            data.to_csv('Dataset/Final_data.csv')
            file = "Dataset/Final_data.csv"
            with open(file, mode='r') as f:
                next(f)
                reader = csv.reader(f, delimiter="\n")
                for i in reader:
                    data = ','.join([value for value in i])
                    self.session.execute("USE {keyspace};".format(keyspace=self.keyspace))
                    self.session.execute(
                        "INSERT INTO {table_name} (ID,X1,X2,X3,X4,X5,X6,X7,X8,Y1,Y2) VALUES ({data});".format(table_name=self.table_name, data=data))
                # print('All Data Entred Into energy Database')
                logger.info('INFO','All The Data Entred Into The {keyspace} Having Table Name {table_name}'.format(format(keyspace=self.keyspace, table_name=self.table_name)))

        except Exception as e:
            raise Exception(f"(insertIntoData) - Their Is Something Wrong About Insert Into Data Method \n" + str(e))

    def getData(self):

        try:

            logger.info('INFO', 'Trying To Get The Data From The DataBase')
            df = pd.DataFrame()
            query = "SELECT * FROM {keyspace}.{table_name};".format(keyspace=self.keyspace,table_name=self.table_name)
            for row in self.session.execute(query):
                df = df.append(pd.DataFrame([row]))
            return df
            logger.info('INFO', 'The Data Import From The Data Base Is Successful')

        except Exception as e:
            raise Exception(f"(getData) - Their Is Something Wrong About getData Method \n" + str(e))
