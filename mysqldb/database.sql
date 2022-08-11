CREATE TABLE user
(
    userid varchar(20),
    username varchar(50),
    followers_count int unsigned,
    followings_count int unsigned,
    full_name varchar(50),
    tracks_count int unsigned,
    profile_link varchar(100),
    playlists_count mediumint unsigned,
    CONSTRAINT Pk_userid PRIMARY KEY (userid)
)

CREATE TABLE tracks
(
    creator_id varchar(20),
    playlist_id varchar(20)
    
)

CREATE TABLE playlists
(
    creator_id varchar(20)
    
)



