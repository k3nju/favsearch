#! /usr/bin/env python
# -*- coding:utf-8 -*-

"""SQL statements module

SQL statements used by db.py are written here.
"""


USERS_TABLE = """
create table users(
  user_id   integer primary key,
  user_name text    not null
);
""";

TWEETS_TABLE = """
create table tweets(
  tweet_id integer primary key,
  user_id  integer not null,
  content  text    not null,
  foreign key( user_id ) references users( user_id )
);
""";

TWEET_FTS_TABLE = """
create virtual table tweets_fts using fts4 (
  tweet_id integer unique not null,
  words    text not null,
  foreign key( tweet_id ) references tweets( tweet_id )
);
""";

URLS_TABLE = """
create table urls(
  tweet_id integer not null,
  url text not null
);
""";

HAS_INSERTED = """
select
  1
from
  tweets
where
  tweet_id = ?;
""";

ADD_USER = """
insert into
  users( user_id, user_name )
select
  ?, ?
where
  not exists(
    select
      *
    from
      users
    where
      user_id = ?
  );
""";

ADD_TWEET = """
insert into
  tweets( tweet_id, user_id, content )
select
  ?, a.user_id, ?
from
  users a
where
  a.user_id = ?
  and not exists(
    select
      *
    from
      tweets b
    where
      b.tweet_id = ?
      and b.user_id = a.user_id
  );  
""";

ADD_FTS = """
insert into
  tweets_fts( tweet_id, words )
select
  a.tweet_id, ?
from
  tweets a
where
  a.tweet_id = ?
  and not exists(
    select
      *
    from
      tweets_fts b
    where
      b.tweet_id = a.tweet_id
  );
""";

ADD_URL = """
insert into
  urls( tweet_id, url )
select
  a.tweet_id, ?
from
  tweets a
where
  a.tweet_id = ?
  and not exists(
    select
      *
    from
      urls b
    where
      b.tweet_id = a.tweet_id
      and b.url = ?
  );
""";

SEARCH = """
select
  c.user_name
  ,b.content
from
  tweets_fts a
inner join
  tweets b
on
  b.tweet_id = a.tweet_id
inner join
  users c
on
  c.user_id = b.user_id
where
  a.words match ?;
""";

SEARCH_BY_USER_NAME = """
select
  c.user_name
  ,b.content
from
  tweets_fts a
inner join
  tweets b
on
  b.tweet_id = a.tweet_id
inner join
  users c
on
  c.user_id = b.user_id
  and c.user_name = ?
where
  a.words match ?;
""";

LISTUP = """
select
  b.user_name
  ,a.content
from
  tweets a
inner join
  users b
on
  b.user_id = a.user_id;
""";

LISTUP_BY_USER_NAME = """
select
  a.user_name
  ,b.content
from
  users a
inner join
  tweets b
on
  b.user_id = a.user_id
where
  a.user_name = ?;
""";
