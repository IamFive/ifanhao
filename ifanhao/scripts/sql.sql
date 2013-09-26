update av_2_actor aa, actors a
set aa.actor_id = a.id
where aa.av_actor = a.name;

update av_2_tag aa, tags a
set aa.tag_id = a.id
where aa.tag = a.name;


update actors a, actors_copy ac
set 
a.birth = ac.birth,
a.height = ac.height,
a.cn_name = ac.cn_name,
a.weight = ac.weight,
a.cup = ac.cup,
a.chest = ac.chest,
a.waist = ac.waist,
a.hip = ac.hip
where a.name = ac.name


update actors a, actors_copy ac
set 
a.avatar = concat(ac.avatar, '.jpg')
where a.name = ac.name
and ac.has_a = 1