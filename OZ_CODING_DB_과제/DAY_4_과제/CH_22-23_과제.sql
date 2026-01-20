-- 요구사항 확인 전 작성
USE pet;

CREATE TABLE owners(
	owner_id INT AUTO_INCREMENT PRIMARY KEY,
    owner_name VARCHAR(50) NOT NULL
);

CREATE TABLE pets(
	pet_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_name VARCHAR(50) NOT NULL,
    owner_id INT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES owners(owner_id)
);

CREATE TABLE rooms(
	room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_number INT NOT NULL UNIQUE,
    room_type VARCHAR(50)
);

CREATE TABLE reservations(
	reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    room_id INT NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    CONSTRAINT chk_reservation_date CHECK (start_date < end_date),
    FOREIGN KEY (pet_id) REFERENCES pets(pet_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

CREATE TABLE services(
	service_id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL,
    reservation_id INT NOT NULL,
    FOREIGN KEY (reservation_id)
    REFERENCES reservations(reservation_id)
    ON DELETE CASCADE
);
-- 여기 시스템에서는 주인,반려동물,룸,예약은 기본 엔티티라서 쉽게 지우지 않고 유지한다.
-- 이는 시스템의 주요한 자산이다.
-- 하지만 예약의 부속 테이터인 서비스만 예약에 종속되므로 ON DELETE CASCADE를 적용한다.


-- 요구사항 확인 후 재작성
USE petHotel;

CREATE TABLE owners(
	owner_id INT AUTO_INCREMENT PRIMARY KEY,
    owner_name VARCHAR(50) NOT NULL,
    contact VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE pets(
	pet_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_name VARCHAR(50) NOT NULL,
    owner_id INT NOT NULL,
    species VARCHAR(50) NOT NULL,
    breed VARCHAR(50) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES owners(owner_id)
);

CREATE TABLE rooms(
	room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_number INT UNIQUE NOT NULL,
    room_type VARCHAR(50),
    price_PerNight DECIMAL(10, 2) NOT NULL
);

CREATE TABLE reservations(
	reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    room_id INT NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    CONSTRAINT chk_reservation_date CHECK (start_date < end_date),
    FOREIGN KEY (pet_id) REFERENCES pets(pet_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

CREATE TABLE services(
	service_id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL,
    reservation_id INT NOT NULL,
    service_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (reservation_id)
    REFERENCES reservations(reservation_id)
    ON DELETE CASCADE
);