USE kochanyeol;

-- employees 테이블을 생성해주세요
-- 	 `속성명 **id의** 자료형은 INT입니다. 추가로 자동으로 1씩 증가하도록 설정하고 기본키로 지정합니다.`
-- 	 `속성명 **name의** 자료형은 VARCHAR(100)입니다.`
-- 	 `속성명 **position의** 자료형은 VARCHAR(100)입니다.`
-- 	 `속성명 **salary의** 자료형은 DECIMAL(10, 2)입니다.`
CREATE TABLE employees (
	id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    position VARCHAR(100),
    salary DECIMAL(10, 2)
);


-- 직원 데이터를 employees에 추가해주세요
INSERT INTO employees (name, position, salary)
VALUES ('혜린', 'PM', 90000),
	   ('은우', 'Frontend', 80000),
       ('가을', 'Backend', 92000),
       ('지수', 'Frontend', 7800),
       ('민혁', 'Frontend', 96000),
       ('하온', 'Backend', 130000);

-- SELECT name, salary FROM employees;

-- Frontend 직책을 가진 직원 중에서 연봉이 90000 이하인 직원의 이름과 연봉을 조회하세요.
SELECT name, salary FROM employees
WHERE position = 'Frontend'
	AND salary <= 90000;

-- 'PM' 직책을 가진 모든 직원의 연봉을 10% 인상한 후 그 결과를 확인하세요. 
UPDATE employees
SET salary = salary * 1.10
WHERE position = 'PM'

-- 인상 결과 확인
SELECT name, position, salary
FROM employees
WHERE position = 'PM';

-- 모든 'Backend' 직책을 가진 직원의 연봉을 5% 인상하세요.
UPDATE employees
SET salary = salary * 1.05
WHERE position = 'Backend'

-- 인상 결과 확인
SELECT name, position, salary
FROM employees
WHERE position = 'Backend';

-- 민혁 사원의 데이터를 삭제하세요.
DELETE FROM employees
WHERE name = '민혁'
LIMIT 1;

-- 모든 직원을 position 별로 그룹화하여 각 직책의 평균 연봉을 계산하세요.
SELECT position, ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY position;

-- employees 테이블을 삭제하세요.
DROP TABLE employees;
