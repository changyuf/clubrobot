select * from club_robot.activities;


SELECT title, start_time, activity_position FROM activities WHERE activity_position = '��ԣʤ��ë���' ORDER BY start_time DESC LIMIT 2;


INSERT INTO activities
  (title, discription, activity_position, start_time, stop_time,
                cost_male, cost_female, max_participants, dead_line, organiser, organiser_phone)
            VALUES
                ('4��14���ܶ�����7:00��ɳ��������ë����ֲ�����', 
                '��ɳ��������ë����ֲ�����', 
                '��ԣʤ��ë���',
                '2015-04-14 19:00', 
                '2015-04-14 21:00',
                25,
                20,
                17,
                '2015-04-14 18:00',
                'David',
                '13601372153');
                
INSERT INTO activities
  (title, discription, activity_position, start_time, stop_time,
                cost_male, cost_female, max_participants, dead_line, organiser, organiser_phone)
            VALUES
                ('4��16����������7:00��ɳ��������ë����ֲ�����', 
                '��ɳ��������ë����ֲ�����', 
                '��ԣʤ��ë���',
                '2015-04-16 19:00', 
                '2015-04-16 21:00',
                25,
                20,
                12,
                '2015-04-16 18:00',
                'David',
                '13601372153');
              
INSERT INTO activities
  (title, discription, activity_position, start_time, stop_time,
                cost_male, cost_female, max_participants, dead_line, organiser, organiser_phone)
            VALUES
                ('4��18����������3:00��ɳ��������ֲ��ܶȻ�����', 
                '��ɳ��������ֲ��ܶȻ�����', 
                '��ԣʤ��ë���',
                '2015-04-18 15:00', 
                '2015-04-18 18:00',
                35,
                30,
                100,
                '2015-04-18 14:00',
                'David',
                '13601372153');

select title, activity_position,start_time,stop_time,cost_male, cost_female, max_participants, dead_line, organiser, organiser_phone
from activities where start_time > '2015-04-09 08:00:00' and start_time < '2015-04-16 08:30:00'

����ͣ� ��ë��
�ʱ�Σ� 2015-04-09 19:00��2015-04-09 21:00
��ص㣺 ��ԣʤ��ë���    
Ԥ�Ʒ��ã� �У�25Ԫ��Ů��20Ԫ
������ѣ� �У�2500ö��Ů��2000ö
�������ƣ� 0/12  
�Ƿ�ɳ����� �ɳ�������ֹʱ�䣺2015-04-09 18:00
����Ҫ�� ��
                

drop table qq_account;

select * from qq_account;

SELECT uin, qq, nick_name, gender, balance, club_level, activity_times, accumulate_points, card, comments, other_comments
            FROM qq_account WHERE qq = '17014162';
            
select count(*) from club_robot.qq_account;

SELECT * FROM club_robot.qq_account where nick_name = 'test';

UPDATE club_robot.qq_account  SET comments = "Ӣ���������������Ρ������ٷ硢���ٶ���������䡢�����޵С����ڵ�һ" WHERE nick_name = 'test';

UPDATE club_robot.qq_account  SET other_comments = "���˵��������۷ǳ��п�" WHERE nick_name = 'test';

update 

SELECT uin, qq, nick_name, gender, balance, club_level, activity_times, accumulate_points, comments, other_comments FROM qq_account
            WHERE uin = '123456';
            
alter table qq_account change  other_comment other_comments varchar(200);

delete  from club_robot.qq_account where uin =3173831764;

INSERT INTO qq_account
                (uin, qq, nick_name, gender, balance,
                level, activity_times, accumulate_points, comments, other_comments)
            VALUES
                ('3173831764', '3173831764', 'ţ������', 'M', 2000,
                1, 0, 10, "��ţ��", "���п�");

INSERT INTO qq_account
                (uin, qq, nick_name, gender, balance,
                level, activity_times, accumulate_points)
            VALUES
                ('3173831764', '3173831764', '��ţ', 'M', 2000,
                1, 0, 10);
                

ALTER TABLE activities ADD checked_out INT NOT NULL DEFAULT 0;