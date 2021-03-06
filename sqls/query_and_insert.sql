select * from club_robot.activities;


SELECT title, start_time, activity_position FROM activities WHERE activity_position = '天裕胜羽毛球馆' ORDER BY start_time DESC LIMIT 2;

INSERT INTO account_bill_details(account_type,account_id,account_name,operator,operate_time,balance_change,balance,comments)
	VALUES(
		'QQ',
		'17014162',
		'test',
		'test_admin',
		'2015-04-14 19:00',
		100,
		100,
		'充值'
	);
	



select title, activity_position,start_time,stop_time,cost_male, cost_female, max_participants, dead_line, organiser, organiser_phone
from activities where start_time > '2015-04-09 08:00:00' and start_time < '2015-04-16 08:30:00'

活动类型： 羽毛球
活动时段： 2015-04-09 19:00至2015-04-09 21:00
活动地点： 天裕胜羽毛球馆    
预计费用： 男：25元；女：20元
羽币消费： 男：2500枚；女：2000枚
人数限制： 0/12  
是否可撤销： 可撤销，截止时间：2015-04-09 18:00
报名要求： 无
                

drop table qq_account;

select * from qq_account;

SELECT uin, qq, nick_name, gender, balance, club_level, activity_times, accumulate_points, card, comments, other_comments
            FROM qq_account WHERE qq = '17014162';
            
select count(*) from club_robot.qq_account;

SELECT * FROM club_robot.qq_account where nick_name = 'test';

UPDATE club_robot.qq_account  SET comments = "英俊潇洒、风流倜傥、玉树临风、年少多金、神勇威武、天下无敌、宇内第一" WHERE qq = '17014162';

UPDATE club_robot.qq_account  SET other_comments = "该人的自我评价非常中肯" WHERE nick_name = 'test';

update 

SELECT uin, qq, nick_name, gender, balance, club_level, activity_times, accumulate_points, comments, other_comments FROM qq_account
            WHERE uin = '123456';
            
alter table qq_account change  other_comment other_comments varchar(200);

delete  from club_robot.qq_account where uin =3173831764;

INSERT INTO qq_account
                (uin, qq, nick_name, gender, balance,
                level, activity_times, accumulate_points, comments, other_comments)
            VALUES
                ('3173831764', '3173831764', '牛逼人物', 'M', 2000,
                1, 0, 10, "很牛逼", "很中肯");

INSERT INTO qq_account
                (uin, qq, nick_name, gender, balance,
                level, activity_times, accumulate_points)
            VALUES
                ('3173831764', '3173831764', '最牛', 'M', 2000,
                1, 0, 10);
                

ALTER TABLE activities ADD checked_out INT NOT NULL DEFAULT 0;