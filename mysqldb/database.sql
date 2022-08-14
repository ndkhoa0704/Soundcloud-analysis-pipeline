CREATE DATABASE scpipe;

USE scpipe;

CREATE TABLE user
(
    user_id varchar(20),
    username varchar(50) NOT NULL,
    followers_count int unsigned default 0,
    followings_count int unsigned default 0,
    full_name varchar(50),
    tracks_count int unsigned default 0,
    profile_link varchar(200),
    playlists_count mediumint unsigned default 0,
    playlist_likes_count mediumint unsigned default 0,
    CONSTRAINT PK_userid PRIMARY KEY (user_id)
);

CREATE TABLE tracks
(
    creator_id varchar(20) NOT NULL,
    playlist_id varchar(20),
    track_id varchar(20),
    likes_count int unsigned default 0,
    created_at timestamp,
    created bool default false,
    dowloadable bool default false,
    track_url varchar(200),
    title varchar(100),
    genre varchar(20),
    duration mediumint unsigned,
    download_count int unsigned,
    like_date timestamp,
    CONSTRAINT PK_track_id PRIMARY KEY (track_id)
);

CREATE TABLE playlists
(
    creator_id varchar(20) NOT NULL,
    playlist_id varchar(20),
    likes_count int unsigned default 0,
    created_at timestamp,
    created bool default false,
    like_date timestamp,
    duration bigint unsigned default 0,
    playlist_url varchar(200),
    track_count mediumint unsigned default 0,
    CONSTRAINT PK_playlist_id PRIMARY KEY (playlist_id)
);

ALTER TABLE playlists
ADD (
    CONSTRAINT FK_playlists_creator 
        FOREIGN KEY (creator_id) REFERENCES user(user_id),
    CONSTRAINT CK_like_date_playlists
        CHECK ((created = true AND like_date IS NOT NULL) OR (created = false AND like_date IS NULL))
);

ALTER TABLE tracks
ADD (
    CONSTRAINT FK_tracks_creator 
        FOREIGN KEY (creator_id) REFERENCES user(user_id),
    CONSTRAINT FK_tracks_playlists 
        FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id),
    CONSTRAINT CK_like_date_tracks
        CHECK ((created = true AND like_date IS NOT NULL) OR (created = false AND like_date IS NULL))
);