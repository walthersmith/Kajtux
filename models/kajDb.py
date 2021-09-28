"""
======================= START OF LICENSE NOTICE =======================
  Copyright (C) 2021 Walther Smith Franco Otero. All Rights Reserved

  NO WARRANTY. THE PRODUCT IS PROVIDED BY DEVELOPER "AS IS" AND ANY
  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL DEVELOPER BE LIABLE FOR
  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
  GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
  IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE PRODUCT, EVEN
  IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
======================== END OF LICENSE NOTICE ========================
  Primary Author: Walther Smith Franco Otero

"""
import logging
import sqlite3

class kajdb ():
    _DATABASE_NAME = 'kajdb.db'
    logging.getLogger(__name__)
            
        
    def __init__(self): 
        pass #no 
    
    def create_tables(self):
        """
         creation table method
        """
        
        users_table = """
            CREATE TABLE users ( 
                user_id	NUMERIC NOT NULL UNIQUE,                
                username	INTEGER NOT NULL,
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(user_id )
            );
        """

        permission_table = """
            CREATE TABLE users_roles ( 
                user_id	INTEGER NOT NULL,
                guild_id INTEGER NOT NULL,
                role_id	INTEGER NOT NULL,
                role_name INTEGER NOT NULL,
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(user_id,guild_id,role_id ),
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            );
        """

        warning_config_table = """
            CREATE TABLE warning_config (
                id INTEGER NOT NULL,
                guild_id	INTEGER NOT NULL,
                limit_warnings	INTEGER NOT NULL DEFAULT 0,
                jail_role  INTEGER NOT NULL DEFAULT 0,
                jail_time INTEGER NOT NULL DEFAULT 0,
                voice_ch_id INTEGER NOT NULL DEFAULT 0,
                text_ch_id INTEGER NOT NULL DEFAULT 0,                
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(id AUTOINCREMENT )
            );
        """
        warning_table = """        
            CREATE TABLE users_warnings ( 
                user_id	INTEGER NOT NULL,
                guild_id	INTEGER NOT NULL,
                warnings	INTEGER NOT NULL DEFAULT 0,
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(user_id,guild_id),
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            );
        """

        warning_log_table = """
            CREATE TABLE warning_log ( 
                id INTEGER,
                user_id	INTEGER,
                guild_id	INTEGER NOT NULL,
                reason	TEXT,
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(id AUTOINCREMENT)
            );
        """

        jail_table ="""
            CREATE TABLE jail (
                user_id	INTEGER NOT NULL,
                guild_id	INTEGER NOT NULL,
                end_date	DATETIME NOT NULL,
                Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(user_id)
            );
        """

        giveaways = """
            CREATE TABLE "giveaways" (
                "id"	INTEGER NOT NULL UNIQUE,
                "title"	TEXT NOT NULL,
                "worth"	REAL,
                "thumbnail"	TEXT,
                "image"	TEXT,
                "description"	TEXT,
                "instructions"	TEXT,
                "open_giveaway_url"	TEXT,
                "published_date"	DATETIME NOT NULL,
                "type"	TEXT,
                "platforms"	TEXT,
                "end_date"	TEXT,
                "users"	INTEGER,
                "status"	TEXT,
                "gamerpower_url"	TEXT,
                "open_giveaway"	TEXT,
                PRIMARY KEY("id")
            );
        """

        test_query = """
        INSERT INTO "main"."warning_config" ("id", "guild_id", "limit_warnings", "jail_role", "jail_time", "voice_ch_id", "text_ch_id", "Timestamp") VALUES ('1', '276918614999695362', '2', '301161280226459648', '1', '854080132020437012', '854020778168025138', '2021-06-15 02:02:47');
        """
        tables = (users_table,permission_table,warning_config_table,warning_table,warning_log_table,jail_table,test_query,giveaways)
        con = self.open_connection()

        for table in tables :
            cur = con.cursor() 
            #print(table)
            cur.execute(table)
        con.commit()
        con.close()


    def open_connection(self):
        return sqlite3.connect(self._DATABASE_NAME)