use project;
alter table t_all_stocks_5year add column `id` int(10) unsigned primary KEY AUTO_INCREMENT;

select *
from t_all_stocks_5year limit 1000;