-- MariaDB dump 10.19  Distrib 10.10.2-MariaDB, for osx10.18 (arm64)
--
-- Host: aconic-gidc.iptime.org    Database: conia
-- ------------------------------------------------------
-- Server version	10.4.8-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `able_target`
--

DROP TABLE IF EXISTS `able_target`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `able_target` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `store_code` varchar(16) NOT NULL,
  `unique_value` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `mobile` varchar(128) DEFAULT NULL,
  `used` varchar(1) DEFAULT 'N',
  PRIMARY KEY (`id`),
  UNIQUE KEY `able_target_store_code_unique_value_uindex` (`store_code`,`unique_value`),
  KEY `fk_able_target_store1_idx` (`store_code`),
  CONSTRAINT `fk_able_target_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=203 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `add_option`
--

DROP TABLE IF EXISTS `add_option`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `add_option` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `origin_price` decimal(10,2) NOT NULL,
  `supply_price` decimal(10,2) NOT NULL,
  `selling_price` decimal(10,2) NOT NULL,
  `status` varchar(2) NOT NULL DEFAULT 'Y',
  `supply_calc_type` varchar(2) DEFAULT 'F' COMMENT '공급가 계산 방식(퍼센트P,고정금액F)',
  `add_option_group_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_add_option_add_option_group1_idx` (`add_option_group_id`),
  CONSTRAINT `fk_add_option_add_option_group1` FOREIGN KEY (`add_option_group_id`) REFERENCES `add_option_group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='추가 옵션';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `add_option_group`
--

DROP TABLE IF EXISTS `add_option_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `add_option_group` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `min_count` int(11) DEFAULT 0,
  `max_count` int(11) DEFAULT 0,
  `member_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_add_option_group_member1_idx` (`member_id`),
  CONSTRAINT `fk_add_option_group_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='추가 옵션 그룹';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `admin_refund`
--

DROP TABLE IF EXISTS `admin_refund`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_refund` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `order_id` bigint(20) unsigned NOT NULL,
  `product_name` varchar(512) NOT NULL,
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `store_code` varchar(45) NOT NULL,
  `store_name` varchar(45) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `member_id` int(10) unsigned NOT NULL,
  `customer_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_admin_refund_order1_idx` (`order_id`),
  KEY `fk_admin_refund_member1_idx` (`member_id`),
  KEY `fk_admin_refund_customer1_idx` (`customer_id`),
  CONSTRAINT `fk_admin_refund_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_admin_refund_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_admin_refund_order1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COMMENT='관리자 환불 내역';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_info`
--

DROP TABLE IF EXISTS `app_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `os` varchar(16) NOT NULL,
  `name` varchar(45) NOT NULL,
  `identifier` varchar(256) NOT NULL,
  `status` varchar(2) NOT NULL,
  `description` varchar(512) DEFAULT NULL,
  `group` varchar(45) DEFAULT NULL,
  `image` varchar(512) DEFAULT NULL,
  `current_ver` varchar(16) DEFAULT NULL,
  `min_ver` varchar(16) DEFAULT NULL,
  `base_url` varchar(512) DEFAULT NULL,
  `cache_use` varchar(2) DEFAULT 'Y',
  `cache_remove_date` datetime DEFAULT NULL,
  `notice` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `badge`
--

DROP TABLE IF EXISTS `badge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `badge` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(8) NOT NULL,
  `color` varchar(8) DEFAULT NULL,
  `img` varchar(512) DEFAULT NULL,
  `shape` varchar(50) DEFAULT NULL,
  `reg_date` datetime DEFAULT current_timestamp(),
  `mod_date` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COMMENT='뱃지';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `brand`
--

DROP TABLE IF EXISTS `brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `brand` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL COMMENT '브랜드 이름',
  `description` text DEFAULT NULL COMMENT '브랜드 설명',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `photo` varchar(512) DEFAULT NULL,
  `pid` int(10) unsigned DEFAULT NULL,
  `status` varchar(2) NOT NULL DEFAULT 'Y',
  PRIMARY KEY (`id`),
  UNIQUE KEY `brand_name_uindex` (`name`),
  KEY `fk_brand_brand1_idx` (`pid`),
  CONSTRAINT `fk_brand_brand1` FOREIGN KEY (`pid`) REFERENCES `brand` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1053 DEFAULT CHARSET=utf8mb4 COMMENT='브랜드';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cart` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `product_option_id` int(10) unsigned NOT NULL,
  `count` int(11) DEFAULT NULL,
  `checked` tinyint(1) DEFAULT 1,
  `reg_date` datetime DEFAULT current_timestamp(),
  `mod_date` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `customer_id` int(10) unsigned NOT NULL,
  `store_code` varchar(16) NOT NULL,
  `type` varchar(2) DEFAULT NULL COMMENT 'D(배송),U(미배송)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_cart_customer_option` (`customer_id`,`product_option_id`,`store_code`),
  KEY `fk_cart_product_option1_idx` (`product_option_id`),
  KEY `fk_cart_customer1_idx` (`customer_id`),
  KEY `fk_cart_store1_idx` (`store_code`),
  CONSTRAINT `fk_cart_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_cart_product_option1` FOREIGN KEY (`product_option_id`) REFERENCES `product_option` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_cart_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=640 DEFAULT CHARSET=utf8mb4 COMMENT='장바구니';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `catalog`
--

DROP TABLE IF EXISTS `catalog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalog` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL COMMENT '이름',
  `description` varchar(255) DEFAULT NULL COMMENT '설명',
  `member_id` int(10) unsigned NOT NULL,
  `open` varchar(2) NOT NULL DEFAULT 'N' COMMENT '열람 범위',
  `status` varchar(2) NOT NULL DEFAULT 'Y',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `fk_catalog_member1_idx` (`member_id`),
  CONSTRAINT `fk_catalog_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4 COMMENT='카탈로그';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `catalog_product`
--

DROP TABLE IF EXISTS `catalog_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalog_product` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `catalog_id` int(10) unsigned NOT NULL,
  `product_id` int(10) unsigned NOT NULL,
  `variation` int(11) NOT NULL DEFAULT 0 COMMENT '가격변동값',
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_ catalog_product` (`catalog_id`,`product_id`),
  KEY `fk_catalog_product_catalog1_idx` (`catalog_id`),
  KEY `fk_catalog_product_product1_idx` (`product_id`),
  CONSTRAINT `fk_catalog_product_catalog1` FOREIGN KEY (`catalog_id`) REFERENCES `catalog` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_catalog_product_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1717 DEFAULT CHARSET=utf8mb4 COMMENT='카탈로그-상품 연결';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `catalog_store`
--

DROP TABLE IF EXISTS `catalog_store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalog_store` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `catalog_id` int(10) unsigned NOT NULL,
  `store_code` varchar(16) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_catalog_store` (`catalog_id`,`store_code`),
  KEY `fk_catalog_store_catalog1_idx` (`catalog_id`),
  KEY `fk_catalog_store_store1_idx` (`store_code`),
  CONSTRAINT `fk_catalog_store_catalog1` FOREIGN KEY (`catalog_id`) REFERENCES `catalog` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_catalog_store_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=274 DEFAULT CHARSET=utf8mb4 COMMENT='카탈로그-상점 연결';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL COMMENT '이름',
  `description` varchar(255) DEFAULT NULL COMMENT '설명',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `photo` varchar(512) DEFAULT NULL,
  `pid` int(10) unsigned DEFAULT NULL,
  `status` varchar(2) NOT NULL DEFAULT 'Y',
  `depth` int(11) DEFAULT NULL,
  `depth1_name` varchar(45) DEFAULT NULL,
  `depth2_name` varchar(45) DEFAULT NULL,
  `depth3_name` varchar(45) DEFAULT NULL,
  `depth4_name` varchar(45) DEFAULT NULL,
  `depth1_id` int(11) DEFAULT NULL,
  `depth2_id` int(11) DEFAULT NULL,
  `depth3_id` int(11) DEFAULT NULL,
  `depth4_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_category_category1_idx` (`pid`),
  CONSTRAINT `fk_category_category1` FOREIGN KEY (`pid`) REFERENCES `category` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5483 DEFAULT CHARSET=utf8mb4 COMMENT='상품 분류';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cert`
--

DROP TABLE IF EXISTS `cert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cert` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `req_token_version_id` varchar(128) DEFAULT NULL COMMENT '요청 구분값',
  `responseno` varchar(32) DEFAULT NULL,
  `authtype` varchar(4) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
  `utf8_name` varchar(64) DEFAULT NULL,
  `birthdate` varchar(128) DEFAULT NULL,
  `gender` varchar(1) DEFAULT NULL,
  `nationalinfo` varchar(1) DEFAULT NULL,
  `mobileco` varchar(1) DEFAULT NULL,
  `mobileno` varchar(128) DEFAULT NULL,
  `ci` varchar(88) DEFAULT NULL,
  `di` varchar(64) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL COMMENT '요청 회원 ID',
  `reg_date` datetime DEFAULT current_timestamp() COMMENT '인증 요청 시간',
  `mod_date` datetime DEFAULT NULL ON UPDATE current_timestamp() COMMENT '인증 완료 시간',
  `status` varchar(2) NOT NULL DEFAULT 'R' COMMENT '상태',
  `ip` varchar(64) DEFAULT NULL COMMENT '요청 아이피',
  `key` varchar(16) DEFAULT NULL COMMENT '암호화 key',
  `iv` varchar(16) DEFAULT NULL COMMENT '암호화 iv',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1093 DEFAULT CHARSET=utf8mb4 COMMENT='본인인증 내역';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cert_sms`
--

DROP TABLE IF EXISTS `cert_sms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cert_sms` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(16) NOT NULL,
  `mobile` varchar(16) NOT NULL,
  `code` varchar(6) NOT NULL,
  `status` varchar(2) NOT NULL DEFAULT 'R',
  `ip` varchar(50) NOT NULL,
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='문자 인증';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `class` (
  `code` varchar(8) NOT NULL COMMENT '코드',
  `name` varchar(45) NOT NULL COMMENT '이름',
  `description` varchar(256) DEFAULT NULL COMMENT '설명',
  `group` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='회원 등급';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `class_permission`
--

DROP TABLE IF EXISTS `class_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `class_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class_code` varchar(8) NOT NULL,
  `permission_code` varchar(128) NOT NULL,
  `target` varchar(16) NOT NULL DEFAULT '*',
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_class_permission_class_code` (`class_code`,`permission_code`),
  KEY `fk_class_permission_class1_idx` (`class_code`),
  KEY `fk_class_permission_permission1_idx` (`permission_code`),
  CONSTRAINT `fk_member_class_permission_class1` FOREIGN KEY (`class_code`) REFERENCES `class` (`code`) ON DELETE CASCADE,
  CONSTRAINT `fk_member_class_permission_permission1` FOREIGN KEY (`permission_code`) REFERENCES `permission` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=utf8mb4 COMMENT='회원등급-권한 연결';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `commission`
--

DROP TABLE IF EXISTS `commission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `commission` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `store_code` varchar(16) DEFAULT NULL,
  `product_id` int(10) unsigned DEFAULT NULL,
  `member_id` int(10) unsigned DEFAULT NULL,
  `type` varchar(2) NOT NULL COMMENT '퍼센트(P) or 고정(F)',
  `value` decimal(10,2) NOT NULL COMMENT '수수료',
  `default` varchar(1) NOT NULL DEFAULT 'N',
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `target` int(10) unsigned NOT NULL COMMENT '수익을 받을 대상',
  `target_type` varchar(10) DEFAULT NULL COMMENT 'CC, CO, PAC',
  `pg_provider` varchar(16) DEFAULT NULL,
  `pg_kind` varchar(16) DEFAULT NULL,
  `kind` varchar(16) DEFAULT NULL COMMENT 'prd 상품, ship 배송비',
  `payment` varchar(2) DEFAULT NULL COMMENT '이익차감[D], 분리지급[S]',
  PRIMARY KEY (`id`),
  KEY `fk_commission_store1_idx` (`store_code`),
  KEY `fk_commission_member1_idx` (`member_id`),
  KEY `fk_commission_product1_idx` (`product_id`),
  KEY `fk_commission_member2_idx` (`target`),
  CONSTRAINT `fk_commission_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_commission_member2` FOREIGN KEY (`target`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_commission_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_commission_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8mb4 COMMENT='수수료';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `common_info`
--

DROP TABLE IF EXISTS `common_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `common_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL COMMENT '이름',
  `contents` text DEFAULT NULL COMMENT '내용',
  `status` varchar(2) NOT NULL DEFAULT 'Y',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `member_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `common_info_member_id_fk` (`member_id`),
  CONSTRAINT `common_info_member_id_fk` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COMMENT='공통 정보';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coupon`
--

DROP TABLE IF EXISTS `coupon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coupon` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(45) NOT NULL COMMENT '코드',
  `name` varchar(45) NOT NULL COMMENT '이름',
  `description` varchar(255) NOT NULL COMMENT '설명',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp() COMMENT '등록일',
  `use_date` datetime DEFAULT NULL COMMENT '사용일',
  `begin_date` datetime DEFAULT NULL COMMENT '시작일',
  `end_date` datetime DEFAULT NULL COMMENT '만료일',
  `use_yn` varchar(1) DEFAULT 'N' COMMENT '사용 여부',
  `amount` decimal(10,2) DEFAULT NULL COMMENT '금액할인',
  `percent` int(11) DEFAULT NULL COMMENT '퍼센트할인',
  `min_price` decimal(10,2) DEFAULT NULL COMMENT '최소주문금액',
  `max_price` decimal(10,2) DEFAULT NULL COMMENT '최대 할인 금액',
  `issuer` int(10) unsigned NOT NULL COMMENT '발행자',
  `coupon_group_id` int(10) unsigned NOT NULL,
  `target` text NOT NULL COMMENT '발행 대상',
  `type` varchar(16) NOT NULL COMMENT 'product, shipping',
  `customer_id` int(10) unsigned NOT NULL,
  `product_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_coupon_member2_idx` (`issuer`),
  KEY `fk_coupon_coupon_group1_idx` (`coupon_group_id`),
  KEY `fk_coupon_customer1_idx` (`customer_id`),
  KEY `fk_coupon_product1_idx` (`product_id`),
  CONSTRAINT `fk_coupon_coupon_group1` FOREIGN KEY (`coupon_group_id`) REFERENCES `coupon_group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_coupon_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_coupon_member2` FOREIGN KEY (`issuer`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_coupon_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4377 DEFAULT CHARSET=utf8mb4 COMMENT='쿠폰';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coupon_group`
--

DROP TABLE IF EXISTS `coupon_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coupon_group` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL COMMENT '이름',
  `description` varchar(255) NOT NULL COMMENT '설명',
  `status` varchar(2) NOT NULL DEFAULT 'Y',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `expire_days` int(11) DEFAULT NULL COMMENT '사용 기한 (일 단위)',
  `begin_date` datetime DEFAULT NULL COMMENT '사용 시작일',
  `begin_time` time DEFAULT NULL COMMENT '사용 시작 시간',
  `end_date` datetime DEFAULT NULL COMMENT '사용 만료일',
  `end_time` time DEFAULT NULL COMMENT '사용 만료 시간',
  `amount` decimal(10,2) DEFAULT NULL COMMENT '금액할인',
  `percent` int(11) DEFAULT NULL COMMENT '퍼센트할인',
  `min_price` decimal(10,2) DEFAULT NULL COMMENT '최소주문금액',
  `max_price` decimal(10,2) DEFAULT NULL COMMENT '최대 할인 금액',
  `issuer` int(10) unsigned NOT NULL COMMENT '발행자',
  `auto` varchar(45) DEFAULT NULL COMMENT '자동 발행 플래그 (join, birth)',
  `publish_limit` int(11) DEFAULT NULL COMMENT '발행 수 제한',
  `publish_begin_date` datetime DEFAULT NULL COMMENT '발행 시작일',
  `publish_end_date` datetime DEFAULT NULL COMMENT '발행 종료일',
  `target` text NOT NULL COMMENT '발행 대상',
  `type` varchar(16) NOT NULL COMMENT 'product, shipping',
  `image` varchar(512) DEFAULT NULL,
  `product_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_coupon_group_product1_idx` (`product_id`),
  CONSTRAINT `fk_coupon_group_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coupon_publish_target`
--

DROP TABLE IF EXISTS `coupon_publish_target`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coupon_publish_target` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `store_code` varchar(16) NOT NULL,
  `coupon_group_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_coupon_publish_target_store1_idx` (`store_code`),
  KEY `fk_coupon_publish_target_coupon_group1_idx` (`coupon_group_id`),
  CONSTRAINT `fk_coupon_publish_target_coupon_group1` FOREIGN KEY (`coupon_group_id`) REFERENCES `coupon_group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_coupon_publish_target_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `coupon_target`
--

DROP TABLE IF EXISTS `coupon_target`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coupon_target` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int(10) unsigned DEFAULT NULL,
  `product_id` int(10) unsigned DEFAULT NULL,
  `coupon_group_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_coupon_target_member1_idx` (`member_id`),
  KEY `fk_coupon_target_product1_idx` (`product_id`),
  KEY `fk_coupon_target_coupon_group1_idx` (`coupon_group_id`),
  CONSTRAINT `fk_coupon_target_coupon_group1` FOREIGN KEY (`coupon_group_id`) REFERENCES `coupon_group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_coupon_target_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_coupon_target_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(45) NOT NULL COMMENT '이메일',
  `password` varchar(256) DEFAULT NULL COMMENT '패스워드',
  `name` varchar(32) DEFAULT NULL COMMENT '이름',
  `nickname` varchar(32) DEFAULT NULL COMMENT '닉네임',
  `mailling` varchar(1) DEFAULT 'N' COMMENT '마케팅 메일 수신여부',
  `sms` varchar(1) DEFAULT 'N' COMMENT '마케팅 문자 수신여부',
  `phone` varchar(128) DEFAULT NULL COMMENT '전화번호',
  `mobile` varchar(128) DEFAULT NULL COMMENT '휴대전화번호',
  `zipcode` varchar(10) DEFAULT NULL COMMENT '우편번호',
  `address` varchar(256) DEFAULT NULL COMMENT '주소',
  `address_detail` varchar(128) DEFAULT NULL COMMENT '상세주소',
  `sex` varchar(1) DEFAULT NULL COMMENT '성별',
  `birthday` date DEFAULT NULL COMMENT '생년월일',
  `recommend` varchar(45) DEFAULT NULL COMMENT '추천인코드',
  `status` varchar(2) DEFAULT 'Y' COMMENT '상태',
  `login_cnt` int(11) DEFAULT 0 COMMENT '로그인횟수',
  `review_cnt` int(11) DEFAULT 0 COMMENT '상품리뷰횟수',
  `order_cnt` int(11) DEFAULT 0 COMMENT '주문횟수',
  `order_sum` int(11) DEFAULT 0 COMMENT '주문금액',
  `lastlogin_date` datetime DEFAULT current_timestamp() COMMENT '마지막 로그인 일시',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `auth_yn` varchar(1) DEFAULT 'N' COMMENT '본인인증 여부',
  `adult_auth` varchar(1) DEFAULT 'N' COMMENT '성인인증 여부',
  `referer` varchar(512) DEFAULT NULL COMMENT '유입경로 full_url',
  `referer_domain` varchar(256) DEFAULT NULL COMMENT '유입경로 도메인',
  `join_platform` varchar(3) DEFAULT NULL COMMENT '가입 플랫폼 (P, M, AOS, IOS)',
  `marketing_agree_date` datetime DEFAULT current_timestamp() COMMENT '마케팅 수신 동의 일시',
  `adult_auth_date` datetime DEFAULT NULL COMMENT '성인인증 일시',
  `sns_naver` varchar(100) DEFAULT NULL,
  `sns_kakao` varchar(100) DEFAULT NULL,
  `sns_google` varchar(100) DEFAULT NULL,
  `sns_facebook` varchar(100) DEFAULT NULL,
  `sns_apple` varchar(100) DEFAULT NULL,
  `sns_payco` varchar(100) DEFAULT NULL,
  `sns_wechat` varchar(100) DEFAULT NULL,
  `grade` varchar(45) DEFAULT NULL COMMENT '등급',
  `refresh_token` varchar(512) DEFAULT NULL,
  `legacy_id` varchar(45) DEFAULT NULL,
  `legacy_pw` varchar(512) DEFAULT NULL,
  `legacy_shop` varchar(45) DEFAULT NULL,
  `ipcc` varchar(32) DEFAULT NULL COMMENT '개인통관고유번호',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2296 DEFAULT CHARSET=utf8mb4 COMMENT='회원';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `delivery_address`
--

DROP TABLE IF EXISTS `delivery_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `delivery_address` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(45) NOT NULL COMMENT '배송지명',
  `name` varchar(45) NOT NULL,
  `address` varchar(255) NOT NULL,
  `address_detail` varchar(255) NOT NULL,
  `zipcode` varchar(16) NOT NULL COMMENT '우편번호',
  `mobile` varchar(255) NOT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `default_yn` varchar(1) NOT NULL DEFAULT 'N',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `customer_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_delivery_address_customer1_idx` (`customer_id`),
  CONSTRAINT `fk_delivery_address_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb4 COMMENT='배송지';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dept`
--

DROP TABLE IF EXISTS `dept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dept` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL COMMENT '이름',
  `description` varchar(255) DEFAULT NULL COMMENT '설명',
  `status` varchar(2) NOT NULL DEFAULT 'Y',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `member_company_id` int(10) unsigned NOT NULL,
  `pid` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_dept_member_company1_idx` (`member_company_id`),
  KEY `fk_dept_dept1_idx` (`pid`),
  CONSTRAINT `fk_dept_dept1` FOREIGN KEY (`pid`) REFERENCES `dept` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_dept_member_company1` FOREIGN KEY (`member_company_id`) REFERENCES `member_company` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COMMENT='관리자 부서';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dept_permission`
--

DROP TABLE IF EXISTS `dept_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dept_permission` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `dept_id` int(10) unsigned NOT NULL,
  `permission_code` varchar(128) NOT NULL,
  `target` varchar(16) NOT NULL DEFAULT '*',
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_dept_permission_dept_code` (`dept_id`,`permission_code`),
  KEY `fk_dept_permission_dept1_idx` (`dept_id`),
  KEY `fk_dept_permission_permission1_idx` (`permission_code`),
  CONSTRAINT `fk_dept_permission_dept1` FOREIGN KEY (`dept_id`) REFERENCES `dept` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_dept_permission_permission1` FOREIGN KEY (`permission_code`) REFERENCES `permission` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='부서 권한';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ecoupon`
--

DROP TABLE IF EXISTS `ecoupon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ecoupon` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `provider` varchar(45) NOT NULL,
  `goods_id` varchar(256) NOT NULL,
  `tr_id` varchar(512) NOT NULL,
  `pin_code` text NOT NULL,
  `period_date` datetime NOT NULL,
  `status` varchar(2) NOT NULL DEFAULT 'Y',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `kind` varchar(45) DEFAULT NULL,
  `duty_code` text DEFAULT NULL,
  `raw_data` text DEFAULT NULL,
  `order_id` bigint(20) unsigned NOT NULL,
  `order_product_id` bigint(20) unsigned NOT NULL,
  `customer_id` int(10) unsigned NOT NULL,
  `order_code` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_ecoupon_order1_idx` (`order_id`),
  KEY `fk_ecoupon_order_product1_idx` (`order_product_id`),
  KEY `fk_ecoupon_customer1_idx` (`customer_id`),
  CONSTRAINT `fk_ecoupon_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_ecoupon_order1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_ecoupon_order_product1` FOREIGN KEY (`order_product_id`) REFERENCES `order_product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `email_history`
--

DROP TABLE IF EXISTS `email_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `email_history` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(16) DEFAULT NULL COMMENT '타입',
  `to` varchar(45) DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL COMMENT '제목',
  `body` text DEFAULT NULL COMMENT '내용',
  `status` varchar(2) DEFAULT NULL COMMENT '상태',
  `mid` varchar(32) DEFAULT NULL COMMENT '전송결과 id',
  `provider` varchar(16) DEFAULT NULL COMMENT '제공 업체',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `res_date` datetime DEFAULT NULL COMMENT '예약일시',
  `can_date` datetime DEFAULT NULL COMMENT '취소일시',
  `member_id` int(10) unsigned DEFAULT NULL,
  `customer_id` int(10) unsigned DEFAULT NULL,
  `order_id` bigint(20) unsigned DEFAULT NULL,
  `store_code` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_email_history_member1_idx` (`member_id`),
  KEY `fk_email_history_order1_idx` (`order_id`),
  KEY `fk_email_history_store1_idx` (`store_code`),
  KEY `fk_email_history_customer1_idx` (`customer_id`),
  CONSTRAINT `fk_email_history_customer10` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_email_history_member10` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_email_history_order10` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_email_history_store10` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2186 DEFAULT CHARSET=utf8mb4 COMMENT='이메일 전송 기록';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `extra_info`
--

DROP TABLE IF EXISTS `extra_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `extra_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(10) unsigned NOT NULL,
  `category` varchar(45) NOT NULL COMMENT '분류',
  `contents` varchar(255) NOT NULL COMMENT '내용',
  PRIMARY KEY (`id`),
  KEY `fk_extra_info_product1_idx` (`product_id`),
  CONSTRAINT `fk_extra_info_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb4 COMMENT='추가 정보';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `faq`
--

DROP TABLE IF EXISTS `faq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `faq` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL COMMENT '제목',
  `contents` text NOT NULL COMMENT '내용',
  `category` varchar(45) DEFAULT NULL COMMENT '분류',
  `status` varchar(2) NOT NULL DEFAULT 'N' COMMENT '상태',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `target` varchar(16) NOT NULL COMMENT '노출 대상 (admin, partner, customer)',
  `store_code` varchar(16) DEFAULT NULL COMMENT '상점에 노출되는 FAQ인 경우',
  `file` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_faq_store1_idx` (`store_code`),
  CONSTRAINT `fk_faq_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COMMENT='자주하는질문';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `faq_category`
--

DROP TABLE IF EXISTS `faq_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `faq_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category` varchar(45) NOT NULL,
  `sort` int(11) NOT NULL DEFAULT 99,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `favorite_product_property`
--

DROP TABLE IF EXISTS `favorite_product_property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `favorite_product_property` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL COMMENT '이름',
  `type` varchar(16) DEFAULT NULL COMMENT '타입',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COMMENT='상품 속성';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `favorite_product_property_detail`
--

DROP TABLE IF EXISTS `favorite_product_property_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `favorite_product_property_detail` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `value` varchar(128) NOT NULL COMMENT '속성값',
  `price` decimal(10,2) NOT NULL COMMENT '가격',
  `code` varchar(45) NOT NULL,
  `favorite_product_property_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_favorite_product_property_detail_favorite_product_proper_idx` (`favorite_product_property_id`),
  CONSTRAINT `fk_favorite_product_property_detail_favorite_product_property1` FOREIGN KEY (`favorite_product_property_id`) REFERENCES `favorite_product_property` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COMMENT='상품 속성 상세';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `count` int(11) NOT NULL DEFAULT 0,
  `safe_count` int(11) NOT NULL DEFAULT 0 COMMENT '안전재고',
  `product_option_id` int(10) unsigned NOT NULL,
  `day_able_count` int(11) DEFAULT NULL COMMENT '일 처리가능수량',
  `use_acc_qty` varchar(1) DEFAULT 'N' COMMENT '누적 수량 사용여부',
  PRIMARY KEY (`id`),
  KEY `fk_inventory_product_option1_idx` (`product_option_id`),
  CONSTRAINT `fk_inventory_product_option1` FOREIGN KEY (`product_option_id`) REFERENCES `product_option` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2143 DEFAULT CHARSET=utf8mb4 COMMENT='재고';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `log_commission`
--

DROP TABLE IF EXISTS `log_commission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_commission` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int(10) unsigned NOT NULL,
  `action` varchar(32) NOT NULL,
  `msg` text NOT NULL,
  `writer` varchar(64) NOT NULL,
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `del` varchar(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`id`),
  KEY `fk_log_commission_member1` (`member_id`),
  CONSTRAINT `fk_log_commission_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COMMENT='수수료 로그';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `log_customer`
--

DROP TABLE IF EXISTS `log_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_customer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(10) unsigned NOT NULL,
  `action` varchar(32) NOT NULL,
  `msg` text NOT NULL,
  `writer` varchar(64) NOT NULL,
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `del` varchar(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`id`),
  KEY `fk_log_customer_customer1_idx` (`customer_id`),
  CONSTRAINT `fk_log_customer_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `log_member`
--

DROP TABLE IF EXISTS `log_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_member` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int(10) unsigned NOT NULL,
  `action` varchar(32) NOT NULL,
  `msg` text NOT NULL,
  `writer` varchar(64) NOT NULL,
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `del` varchar(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`id`),
  KEY `fk_log_member_member1_idx` (`member_id`),
  KEY `fk_log_commission_member1_idx` (`member_id`),
  CONSTRAINT `fk_log_member_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1255 DEFAULT CHARSET=utf8mb4 COMMENT='상품 로그';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `log_order`
--

DROP TABLE IF EXISTS `log_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_order` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `order_id` bigint(20) unsigned NOT NULL,
  `action` varchar(32) NOT NULL,
  `msg` text NOT NULL,
  `writer` varchar(64) NOT NULL,
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `del` varchar(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`id`),
  KEY `fk_log_order_order1_idx` (`order_id`),
  CONSTRAINT `fk_log_order_order1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=42248 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `log_product`
--

DROP TABLE IF EXISTS `log_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_product` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(10) unsigned NOT NULL,
  `action` varchar(32) NOT NULL,
  `msg` text NOT NULL,
  `writer` varchar(64) NOT NULL,
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `del` varchar(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`id`),
  KEY `fk_log_product_product1_idx` (`product_id`),
  CONSTRAINT `fk_log_product_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4172 DEFAULT CHARSET=utf8mb4 COMMENT='상품 로그';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `log_store`
--

DROP TABLE IF EXISTS `log_store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_store` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `store_code` varchar(16) NOT NULL,
  `action` varchar(32) NOT NULL,
  `msg` text NOT NULL,
  `writer` varchar(64) NOT NULL,
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `del` varchar(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`id`),
  KEY `fk_log_store_store1_idx` (`store_code`),
  CONSTRAINT `fk_log_store_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7098 DEFAULT CHARSET=utf8mb4 COMMENT='상점 로그';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(45) NOT NULL COMMENT '이메일',
  `password` varchar(256) DEFAULT NULL COMMENT '패스워드',
  `name` varchar(32) DEFAULT NULL COMMENT '이름',
  `nickname` varchar(32) DEFAULT NULL COMMENT '닉네임',
  `mailling` varchar(1) DEFAULT 'N' COMMENT '마케팅 메일 수신여부',
  `sms` varchar(1) DEFAULT 'N' COMMENT '마케팅 문자 수신여부',
  `phone` varchar(128) DEFAULT NULL COMMENT '전화번호',
  `mobile` varchar(128) DEFAULT NULL COMMENT '휴대전화번호',
  `zipcode` varchar(10) DEFAULT NULL COMMENT '우편번호',
  `address` varchar(256) DEFAULT NULL COMMENT '주소',
  `address_detail` varchar(128) DEFAULT NULL COMMENT '상세주소',
  `sex` varchar(1) DEFAULT NULL COMMENT '성별',
  `birthday` date DEFAULT NULL COMMENT '생년월일',
  `recommend` varchar(45) DEFAULT NULL COMMENT '추천인코드',
  `status` varchar(2) DEFAULT 'Y' COMMENT '상태',
  `login_cnt` int(11) DEFAULT 0 COMMENT '로그인횟수',
  `review_cnt` int(11) DEFAULT 0 COMMENT '상품리뷰횟수',
  `order_cnt` int(11) DEFAULT 0 COMMENT '주문횟수',
  `order_sum` int(11) DEFAULT 0 COMMENT '주문금액',
  `lastlogin_date` datetime DEFAULT current_timestamp() COMMENT '마지막 로그인 일시',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `auth_yn` varchar(1) DEFAULT 'N' COMMENT '본인인증 여부',
  `adult_auth` varchar(1) DEFAULT 'N' COMMENT '성인인증 여부',
  `referer` varchar(512) DEFAULT NULL COMMENT '유입경로 full_url',
  `referer_domain` varchar(256) DEFAULT NULL COMMENT '유입경로 도메인',
  `join_platform` varchar(3) DEFAULT NULL COMMENT '가입 플랫폼 (P, M, AOS, IOS)',
  `marketing_agree_date` datetime DEFAULT current_timestamp() COMMENT '마케팅 수신 동의 일시',
  `adult_auth_date` datetime DEFAULT NULL COMMENT '성인인증 일시',
  `sns_naver` varchar(100) DEFAULT NULL,
  `sns_kakao` varchar(100) DEFAULT NULL,
  `sns_google` varchar(100) DEFAULT NULL,
  `sns_facebook` varchar(100) DEFAULT NULL,
  `sns_apple` varchar(100) DEFAULT NULL,
  `sns_payco` varchar(100) DEFAULT NULL,
  `bank` varchar(16) DEFAULT NULL COMMENT '환불용 계좌 은행',
  `account` varchar(45) DEFAULT NULL COMMENT '환불용 계좌',
  `admin_yn` varchar(1) NOT NULL DEFAULT 'N' COMMENT '관리자 여부',
  `otp` varchar(40) DEFAULT NULL,
  `grade` varchar(45) DEFAULT NULL COMMENT '등급',
  `refresh_token` varchar(512) DEFAULT NULL,
  `partner` varchar(2) DEFAULT 'N' COMMENT '파트너 회원 [N, Y, R(승인대기)]',
  `memo` varchar(255) DEFAULT NULL COMMENT '관리자 메모',
  `confirm_pass` varchar(16) DEFAULT NULL COMMENT '직원 확인용 패스워드',
  `shop_yn` varchar(2) DEFAULT 'N' COMMENT '매장 여부',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=191 DEFAULT CHARSET=utf8mb4 COMMENT='회원';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_class`
--

DROP TABLE IF EXISTS `member_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_class` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int(10) unsigned NOT NULL,
  `class_code` varchar(8) NOT NULL,
  `grade` varchar(45) DEFAULT NULL COMMENT '등급',
  PRIMARY KEY (`id`),
  KEY `fk_member_grade_member1_idx` (`member_id`),
  KEY `fk_member_class_class1_idx` (`class_code`),
  CONSTRAINT `fk_member_class_class1` FOREIGN KEY (`class_code`) REFERENCES `class` (`code`) ON DELETE CASCADE,
  CONSTRAINT `fk_member_grade_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=206 DEFAULT CHARSET=utf8mb4 COMMENT='회원-등급 연결';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_company`
--

DROP TABLE IF EXISTS `member_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_company` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int(10) unsigned NOT NULL,
  `name` varchar(45) DEFAULT NULL COMMENT '이름',
  `ceo` varchar(45) DEFAULT NULL COMMENT '대표자명',
  `reg_no` varchar(45) DEFAULT NULL COMMENT '사업자등록번호',
  `biz_type` varchar(45) DEFAULT NULL COMMENT '업태',
  `biz_item` varchar(45) DEFAULT NULL COMMENT '업종',
  `zipcode` varchar(10) DEFAULT NULL COMMENT '우편번호',
  `address` varchar(256) DEFAULT NULL COMMENT '주소',
  `address_detail` varchar(128) DEFAULT NULL COMMENT '주소상세',
  `phone` varchar(32) DEFAULT NULL COMMENT '대표자 전화번호',
  `mobile` varchar(32) DEFAULT NULL COMMENT '대표자 휴대전화',
  `corp_type` varchar(3) NOT NULL COMMENT '사업자 종류 (개인(P),법인(B),개인사업자(PB),개인사업자간이과세(PBS))',
  `corp_number` varchar(45) DEFAULT NULL COMMENT '법인번호(주민번호)',
  `tax_email` varchar(128) DEFAULT NULL COMMENT '계산서 이메일',
  `bank` varchar(16) DEFAULT NULL COMMENT '은행',
  `account` varchar(45) DEFAULT NULL COMMENT '계좌번호',
  `bank_user` varchar(45) DEFAULT NULL COMMENT '예금주',
  `photo_reg` varchar(512) DEFAULT NULL COMMENT '사업자등록증 사진',
  `photo_bank` varchar(512) DEFAULT NULL COMMENT '통장 사본 사진',
  `status` varchar(2) NOT NULL DEFAULT 'R' COMMENT '사업자 승인 여부',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `manager_name` varchar(32) DEFAULT NULL COMMENT '담당자명',
  `manager_phone` varchar(32) DEFAULT NULL COMMENT '담당자 전화번호',
  `manager_mobile` varchar(32) DEFAULT NULL COMMENT '담당자 휴대전화',
  `manager_email` varchar(128) DEFAULT NULL COMMENT '담당자 이메일',
  `settlement_name` varchar(32) DEFAULT NULL COMMENT '정산 담당자명',
  `settlement_phone` varchar(32) DEFAULT NULL COMMENT '정산 담당자 전화번호',
  `settlement_mobile` varchar(32) DEFAULT NULL COMMENT '정산 담당자 휴대전화',
  `settlement_email` varchar(128) DEFAULT NULL COMMENT '정산 담당자 이메일',
  `cs_name` varchar(32) DEFAULT NULL COMMENT 'CS 담당자명',
  `cs_phone` varchar(32) DEFAULT NULL COMMENT 'CS 담당자 전화번호',
  `cs_mobile` varchar(32) DEFAULT NULL COMMENT 'CS 담당자 휴대전화',
  `cs_email` varchar(128) DEFAULT NULL COMMENT 'CS 담당자 이메일',
  `network_reg_no` varchar(24) DEFAULT NULL COMMENT '통신판매업 신고번호',
  PRIMARY KEY (`id`),
  KEY `fk_member_company_member_idx` (`member_id`),
  CONSTRAINT `fk_member_company_member` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=173 DEFAULT CHARSET=utf8mb4 COMMENT='회원 사업자 정보';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_member`
--

DROP TABLE IF EXISTS `member_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_member` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int(10) unsigned NOT NULL,
  `pid` int(10) unsigned NOT NULL COMMENT '상위 회원',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_member_member_link` (`member_id`,`pid`),
  KEY `fk_member_member_member1_idx` (`member_id`),
  KEY `fk_member_member_member2_idx` (`pid`),
  CONSTRAINT `fk_member_member_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_member_member_member2` FOREIGN KEY (`pid`) REFERENCES `member` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COMMENT='회원-회원 연결';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_permission`
--

DROP TABLE IF EXISTS `member_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_permission` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int(10) unsigned NOT NULL,
  `permission_code` varchar(128) NOT NULL,
  `target` varchar(16) NOT NULL DEFAULT '*',
  `exclude` varchar(1) DEFAULT 'N' COMMENT '제외 플래그',
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_member_permission_member_code` (`member_id`,`permission_code`),
  KEY `fk_member_permission_member1_idx` (`member_id`),
  KEY `fk_member_permission_permission1_idx` (`permission_code`),
  CONSTRAINT `fk_member_permission_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_member_permission_permission1` FOREIGN KEY (`permission_code`) REFERENCES `permission` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=143 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_store`
--

DROP TABLE IF EXISTS `member_store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_store` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `confirm` varchar(1) NOT NULL DEFAULT 'N',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `store_code` varchar(16) NOT NULL,
  `customer_id` int(10) unsigned NOT NULL,
  `recommander_member_id` int(10) unsigned DEFAULT NULL COMMENT '상점 이용 추천 회원',
  `value` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_customer_store` (`customer_id`,`store_code`),
  KEY `fk_member_store_member1_idx` (`recommander_member_id`),
  KEY `fk_member_store_store1_idx` (`store_code`),
  KEY `fk_member_store_customer1_idx` (`customer_id`),
  CONSTRAINT `fk_member_store_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_member_store_member1` FOREIGN KEY (`recommander_member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_member_store_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2279 DEFAULT CHARSET=utf8mb4 COMMENT='이용 신청 상점';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `member_worker`
--

DROP TABLE IF EXISTS `member_worker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_worker` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int(10) unsigned NOT NULL,
  `dept_id` int(10) unsigned NOT NULL,
  `member_company_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_member_company_dept` (`member_id`,`dept_id`),
  KEY `fk_member_worker_member1_idx` (`member_id`),
  KEY `fk_member_worker_dept1_idx` (`dept_id`),
  KEY `fk_member_worker_member_company1_idx` (`member_company_id`),
  CONSTRAINT `fk_member_worker_dept1` FOREIGN KEY (`dept_id`) REFERENCES `dept` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_member_worker_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_member_worker_member_company1` FOREIGN KEY (`member_company_id`) REFERENCES `member_company` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='회원 조직 직원 연결';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `depth` int(11) NOT NULL,
  `menu_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_menu_menu1_idx` (`menu_id`),
  CONSTRAINT `fk_menu_menu1` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `menu_class`
--

DROP TABLE IF EXISTS `menu_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `menu_class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `menu_id` int(11) NOT NULL,
  `class_code` varchar(8) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_menu_class_menu1_idx` (`menu_id`),
  KEY `fk_menu_class_class1_idx` (`class_code`),
  CONSTRAINT `fk_menu_class_class1` FOREIGN KEY (`class_code`) REFERENCES `class` (`code`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_menu_class_menu1` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=155 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notice`
--

DROP TABLE IF EXISTS `notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notice` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL COMMENT '제목',
  `contents` text NOT NULL COMMENT '내용',
  `pin` varchar(1) DEFAULT 'N' COMMENT '상위 고정',
  `sort` int(11) DEFAULT 99 COMMENT '순서',
  `status` varchar(2) DEFAULT NULL COMMENT '상태',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `target` varchar(16) NOT NULL COMMENT '노출 대상 (admin, partner, customer)',
  `member_id` int(10) unsigned NOT NULL,
  `store_code` varchar(16) DEFAULT NULL,
  `file` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_notice_member1_idx` (`member_id`),
  KEY `fk_notice_store1_idx` (`store_code`),
  CONSTRAINT `fk_notice_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_notice_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COMMENT='공지사항';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notice_info`
--

DROP TABLE IF EXISTS `notice_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notice_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(10) unsigned NOT NULL,
  `item` varchar(255) NOT NULL COMMENT '품목',
  `category` varchar(45) NOT NULL COMMENT '항목',
  `contents` varchar(255) NOT NULL COMMENT '내용',
  `sort` int(11) NOT NULL DEFAULT 99 COMMENT '순서',
  PRIMARY KEY (`id`),
  KEY `fk_notice_info_product1_idx` (`product_id`),
  CONSTRAINT `fk_notice_info_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4026 DEFAULT CHARSET=utf8mb4 COMMENT='상품정보제공고시';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notice_info_template`
--

DROP TABLE IF EXISTS `notice_info_template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notice_info_template` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `category` varchar(45) NOT NULL COMMENT '항목',
  `item` varchar(255) NOT NULL COMMENT '품목',
  `num` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=383 DEFAULT CHARSET=utf8mb4 COMMENT='상품정보제공고시 템플릿';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `option_value`
--

DROP TABLE IF EXISTS `option_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `option_value` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(32) DEFAULT NULL COMMENT '타입',
  `name` varchar(64) DEFAULT NULL COMMENT '이름',
  `value` varchar(128) DEFAULT NULL COMMENT '값',
  `sort` int(11) DEFAULT 99 COMMENT '순서',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COMMENT='옵션값 모음';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order` (
  `id` bigint(20) unsigned NOT NULL,
  `store_code` varchar(16) NOT NULL,
  `origin_order_id` bigint(20) unsigned DEFAULT NULL COMMENT '연결된 주문',
  `origin_amount` decimal(10,2) NOT NULL COMMENT '정상 판매가 금액',
  `raw_amount` decimal(10,2) NOT NULL COMMENT '결제 대상 금액',
  `final_amount` decimal(10,2) NOT NULL COMMENT '최종 결제 금액',
  `tex_free_amount` decimal(10,2) DEFAULT NULL COMMENT '비과세 금액',
  `tax_rate` varchar(3) DEFAULT NULL COMMENT '부가세율',
  `discount` decimal(10,2) DEFAULT NULL COMMENT '할인 금액',
  `status` varchar(2) NOT NULL COMMENT '상태',
  `user_name` varchar(32) DEFAULT NULL COMMENT '주문자명',
  `user_phone` varchar(20) DEFAULT NULL COMMENT '주문자 전화번호',
  `user_mobile` varchar(20) DEFAULT NULL COMMENT '주문자 휴대전화',
  `user_email` varchar(100) DEFAULT NULL COMMENT '주문자 이메일',
  `recipient_name` varchar(32) DEFAULT NULL COMMENT '수령인',
  `recipient_phone` varchar(20) DEFAULT NULL COMMENT '수령인 전화번호',
  `recipient_mobile` varchar(20) DEFAULT NULL COMMENT '수령인 휴대전화',
  `shipping_cost` decimal(10,2) DEFAULT NULL COMMENT '배송비결제금액',
  `shipping_cost_post` decimal(10,2) DEFAULT NULL COMMENT '착불배송비',
  `shipping_condition` varchar(255) DEFAULT NULL COMMENT '배송비 조건',
  `shipping_msg` varchar(255) DEFAULT NULL COMMENT '배송메세지',
  `zipcode` varchar(10) DEFAULT NULL COMMENT '우편번호',
  `address` varchar(255) DEFAULT NULL COMMENT '주소',
  `address_detail` varchar(128) DEFAULT NULL COMMENT '주소상세',
  `coupon_discount` decimal(10,2) DEFAULT NULL COMMENT '쿠폰할인금액',
  `step_type` varchar(10) DEFAULT NULL COMMENT '(direct:바로구매, cart:장바구니구매)',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `client_type` varchar(10) DEFAULT NULL COMMENT 'P, M, AOS, IOS',
  `referer` varchar(45) DEFAULT NULL COMMENT '유입매체',
  `referer_url` varchar(255) DEFAULT NULL COMMENT '유입 url',
  `total_ea` int(11) DEFAULT NULL COMMENT '총삼품수',
  `total_kind` int(11) DEFAULT NULL COMMENT '총삼품종류',
  `ipcc_code` varchar(45) DEFAULT NULL COMMENT '개인통관고유번호',
  `ip` varchar(50) DEFAULT NULL,
  `settlement_date` datetime DEFAULT NULL COMMENT '정산 처리일시',
  `password` varchar(256) DEFAULT NULL COMMENT '비회원 주문일 경우 비밀번호',
  `cert_id` int(10) unsigned DEFAULT NULL,
  `customer_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_order_order1_idx` (`origin_order_id`),
  KEY `fk_order_store1_idx` (`store_code`),
  KEY `fk_order_cert1_idx` (`cert_id`),
  KEY `fk_order_customer1_idx` (`customer_id`),
  CONSTRAINT `fk_order_cert1` FOREIGN KEY (`cert_id`) REFERENCES `cert` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_order1` FOREIGN KEY (`origin_order_id`) REFERENCES `order` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='주문';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `order_coupon`
--

DROP TABLE IF EXISTS `order_coupon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_coupon` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `order_id` bigint(20) unsigned NOT NULL,
  `coupon_id` bigint(20) unsigned NOT NULL,
  `discount` decimal(10,2) NOT NULL DEFAULT 0.00,
  `order_product_id` bigint(20) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_order_coupon_order_coupon` (`order_id`,`coupon_id`),
  KEY `fk_order_coupon_order1_idx` (`order_id`),
  KEY `fk_order_coupon_coupon1_idx` (`coupon_id`),
  KEY `fk_order_coupon_order_product1` (`order_product_id`),
  CONSTRAINT `fk_order_coupon_coupon1` FOREIGN KEY (`coupon_id`) REFERENCES `coupon` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_coupon_order1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_coupon_order_product1` FOREIGN KEY (`order_product_id`) REFERENCES `order_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COMMENT='주문-쿠폰 연결';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `order_product`
--

DROP TABLE IF EXISTS `order_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_product` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `order_id` bigint(20) unsigned NOT NULL,
  `product_option_id` int(10) unsigned NOT NULL,
  `product_code` varchar(255) NOT NULL,
  `ea` int(11) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `status` varchar(3) NOT NULL DEFAULT 'Y',
  `seller_title` varchar(45) NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `product_description` varchar(255) NOT NULL,
  `product_thumbnail` varchar(512) NOT NULL,
  `origin_price` decimal(10,2) DEFAULT NULL,
  `order_shipping_id` bigint(20) unsigned DEFAULT NULL,
  `member_id` int(10) unsigned NOT NULL COMMENT '공급자 회원 ID',
  `product_id` int(10) unsigned NOT NULL,
  `settlement_date` datetime DEFAULT NULL COMMENT '정산처리일',
  `use_end_date` datetime DEFAULT NULL COMMENT '사용 만료일',
  `use_date` datetime DEFAULT NULL COMMENT '사용 일시',
  `code` varchar(128) DEFAULT NULL COMMENT '발행 코드',
  `user_name` varchar(32) DEFAULT NULL,
  `user_phone` varchar(16) DEFAULT NULL,
  `user_email` varchar(45) DEFAULT NULL,
  `type` varchar(16) DEFAULT NULL COMMENT '상품 유형',
  `discount` decimal(10,2) DEFAULT NULL,
  `complete_date` datetime DEFAULT NULL COMMENT '구매 확정일',
  `balance` int(11) DEFAULT 0 COMMENT '잔액',
  PRIMARY KEY (`id`),
  KEY `fk_order_product_option_order1_idx` (`order_id`),
  KEY `fk_order_product_option_product_option1_idx` (`product_option_id`),
  KEY `fk_order_product_order_shipping1_idx` (`order_shipping_id`),
  KEY `fk_order_product_member1_idx` (`member_id`),
  KEY `fk_order_product_product1` (`product_id`),
  CONSTRAINT `fk_order_product_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_product_option_order1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_product_option_product_option1` FOREIGN KEY (`product_option_id`) REFERENCES `product_option` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_order_product_order_shipping1` FOREIGN KEY (`order_shipping_id`) REFERENCES `order_shipping` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_product_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1006 DEFAULT CHARSET=utf8mb4 COMMENT='주문-상품옵션 연결';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`lsj`@`%`*/ /*!50003 trigger inventory_trigger after insert on order_product
    for each row begin
    update inventory set count = count - NEW.ea where product_option_id = NEW.product_option_id;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`lsj`@`%`*/ /*!50003 trigger cancel_inventory_trigger
    after update on order_product
    for each row
    begin
        if NEW.status = 'CD' and OLD.type != 'DP' and (select inven_use from product as p where p.id = OLD.product_id) = 'Y' then
            update inventory set count = count + OLD.ea where product_option_id = OLD.product_option_id;
        end if;
    end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `order_re`
--

DROP TABLE IF EXISTS `order_re`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_re` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `order_id` bigint(20) unsigned NOT NULL,
  `type` varchar(16) NOT NULL COMMENT '타입, return, refund, exchange',
  `contents` text DEFAULT NULL,
  `category` varchar(128) DEFAULT NULL,
  `memo` text DEFAULT NULL,
  `status` varchar(2) NOT NULL DEFAULT 'R',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `end_date` datetime DEFAULT NULL,
  `refund_amount` decimal(10,2) DEFAULT NULL,
  `pay_type` varchar(45) DEFAULT NULL,
  `refund_date` datetime DEFAULT NULL,
  `log` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_order_rre_order1_idx` (`order_id`),
  CONSTRAINT `fk_order_rre_order1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COMMENT='주문 반품교환 요청';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `order_re_product`
--

DROP TABLE IF EXISTS `order_re_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_re_product` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `order_re_id` int(10) unsigned NOT NULL,
  `order_product_id` bigint(20) unsigned NOT NULL,
  `reg_date` datetime DEFAULT current_timestamp(),
  `end_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_order_re_product_order_product1_idx` (`order_product_id`),
  KEY `fk_order_re_product_order_re1_idx` (`order_re_id`),
  CONSTRAINT `fk_order_re_product_order_product1` FOREIGN KEY (`order_product_id`) REFERENCES `order_product` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_order_re_product_order_re1` FOREIGN KEY (`order_re_id`) REFERENCES `order_re` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `order_sheet`
--

DROP TABLE IF EXISTS `order_sheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_sheet` (
  `id` varchar(36) NOT NULL,
  `store_code` varchar(16) NOT NULL,
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `step_type` varchar(10) DEFAULT NULL COMMENT '생성 경로',
  `customer_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_order_sheet_store1_idx` (`store_code`),
  KEY `fk_order_sheet_customer1_idx` (`customer_id`),
  KEY `order_sheet_reg_date_index` (`reg_date`),
  CONSTRAINT `fk_order_sheet_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_order_sheet_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='주문서';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `order_sheet_product`
--

DROP TABLE IF EXISTS `order_sheet_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_sheet_product` (
  `id` varchar(36) NOT NULL,
  `order_sheet_id` varchar(36) NOT NULL,
  `product_option_id` int(10) unsigned NOT NULL,
  `amount` decimal(10,2) NOT NULL COMMENT '금액',
  `ea` int(11) NOT NULL COMMENT '수량',
  `coupon_id` bigint(20) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_order_sheet_product_order_sheet1_idx` (`order_sheet_id`),
  KEY `fk_order_sheet_product_product_option1_idx` (`product_option_id`),
  KEY `order_sheet_product_coupon_id_fk` (`coupon_id`),
  CONSTRAINT `fk_order_sheet_product_order_sheet1` FOREIGN KEY (`order_sheet_id`) REFERENCES `order_sheet` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_sheet_product_product_option1` FOREIGN KEY (`product_option_id`) REFERENCES `product_option` (`id`) ON DELETE CASCADE,
  CONSTRAINT `order_sheet_product_coupon_id_fk` FOREIGN KEY (`coupon_id`) REFERENCES `coupon` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='주문서 상품';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `order_shipping`
--

DROP TABLE IF EXISTS `order_shipping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_shipping` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `provider` varchar(45) DEFAULT NULL COMMENT '운송업체',
  `provider_code` varchar(16) DEFAULT NULL,
  `number` varchar(45) DEFAULT NULL COMMENT '운송번호',
  `status` varchar(2) DEFAULT NULL COMMENT '상태',
  `cost` decimal(10,2) NOT NULL COMMENT '요금',
  `shipping_type` varchar(10) NOT NULL COMMENT '배송타입',
  `pay_type` varchar(4) NOT NULL COMMENT '선불(pre), 후불(post)',
  `order_id` bigint(20) unsigned NOT NULL,
  `member_id` int(10) unsigned NOT NULL COMMENT '공급자 회원 ID',
  `shipping_info_id` int(10) unsigned NOT NULL,
  `settlement_date` datetime DEFAULT NULL COMMENT '정산처리일',
  `number_reg_date` datetime DEFAULT NULL COMMENT '송장 등록일',
  `complete_date` datetime DEFAULT NULL COMMENT '배송 완료일',
  PRIMARY KEY (`id`),
  KEY `fk_order_shipping_order1_idx` (`order_id`),
  KEY `fk_order_shipping_member1_idx` (`member_id`),
  KEY `fk_order_shipping_shipping_info1_idx` (`shipping_info_id`),
  CONSTRAINT `fk_order_shipping_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_shipping_order1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_shipping_shipping_info1` FOREIGN KEY (`shipping_info_id`) REFERENCES `shipping_info` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=331 DEFAULT CHARSET=utf8mb4 COMMENT='주문 상품 배송';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `payco_auth_code`
--

DROP TABLE IF EXISTS `payco_auth_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payco_auth_code` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `store_code` varchar(16) NOT NULL,
  `code` varchar(45) NOT NULL,
  `memo` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_payco_auth_code_store1_idx` (`store_code`),
  CONSTRAINT `fk_payco_auth_code_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='페이코 임직원 구분 코드';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permission` (
  `code` varchar(128) NOT NULL COMMENT '코드',
  `name` varchar(45) NOT NULL COMMENT '이름',
  `description` varchar(255) NOT NULL COMMENT '설명',
  `type` varchar(2) NOT NULL COMMENT '권한 타입\nMember = B, Admin = A',
  `category` varchar(45) DEFAULT NULL,
  `group` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='권한';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pg_cancel`
--

DROP TABLE IF EXISTS `pg_cancel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pg_cancel` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `pg_info_order_id` bigint(20) unsigned NOT NULL,
  `tno` varchar(45) DEFAULT NULL,
  `type` varchar(10) NOT NULL,
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `amount` int(11) NOT NULL,
  `remain` int(11) DEFAULT NULL,
  `part_seq` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_pg_cancel_pg_info1_idx` (`pg_info_order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=149 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pg_info`
--

DROP TABLE IF EXISTS `pg_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pg_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `order_id` bigint(20) unsigned NOT NULL,
  `provider` varchar(16) NOT NULL COMMENT 'PG사',
  `kind` varchar(16) NOT NULL COMMENT '결제 방법',
  `tid` varchar(45) DEFAULT NULL COMMENT 'PG사 트랜잭션 ID',
  `amount` int(11) NOT NULL,
  `remain_amount` int(11) NOT NULL DEFAULT 0,
  `app_time` varchar(16) NOT NULL COMMENT '승인 시간',
  `deposit_yn` varchar(1) DEFAULT 'N' COMMENT '무통장 입금 여부',
  `deposit_date` datetime DEFAULT NULL COMMENT '무통장 입금 일시',
  `deposit_name` varchar(45) DEFAULT NULL COMMENT '무통장 입금자명',
  `bank_account` varchar(100) DEFAULT NULL COMMENT '무통장 입금계좌정보',
  `virtual_account` varchar(255) DEFAULT NULL COMMENT '가상계좌정보',
  `virtual_date` datetime DEFAULT NULL COMMENT '가상계좌입금제한일',
  `card_app_num` varchar(45) DEFAULT NULL COMMENT '신용카드 승인번호',
  `card_name` varchar(45) DEFAULT NULL COMMENT '신용카드 발급사명',
  `card_no` varchar(45) DEFAULT NULL COMMENT '신용카드 번호',
  `card_quota` varchar(8) DEFAULT NULL COMMENT '신용카드 할부 기간',
  `card_partcanc_yn` varchar(2) DEFAULT NULL COMMENT '신용카드 부분취소 가능 유무',
  `card_bin_type_01` varchar(2) DEFAULT NULL COMMENT '카드구분 개인: 0 / 법인: 1',
  `card_bin_type_02` varchar(2) DEFAULT NULL COMMENT '카드구분 일반: 0 / 체크: 1',
  `cash_authno` varchar(16) DEFAULT NULL COMMENT '현금영수증 승인번호',
  `cash_no` varchar(16) DEFAULT NULL COMMENT '현금영수증 거래번호',
  `bankname` varchar(20) DEFAULT NULL COMMENT '은행 명',
  `commid` varchar(8) DEFAULT NULL COMMENT '휴대폰 결제 통신사 코드',
  `mobile_no` varchar(11) DEFAULT NULL COMMENT '휴대폰 결제 휴대폰 번호',
  `cancel_type` varchar(10) DEFAULT NULL COMMENT '취소 타입(all, part)',
  `cancel_date` datetime DEFAULT NULL COMMENT '취소 시각',
  `cancel_mny` int(11) DEFAULT NULL COMMENT '취소 금액',
  `cancel_part_seq` varchar(32) DEFAULT NULL COMMENT '부분취소 일련번호',
  `cancel_key` varchar(128) DEFAULT NULL COMMENT '취소 키',
  `raw_data` text DEFAULT NULL COMMENT '결제 데이터',
  PRIMARY KEY (`id`),
  KEY `pg_info_order_id_fk` (`order_id`),
  CONSTRAINT `pg_info_order_id_fk` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=510 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pg_info_sub`
--

DROP TABLE IF EXISTS `pg_info_sub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pg_info_sub` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `pg_info_id` int(10) unsigned NOT NULL,
  `kind` varchar(45) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `tno` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_pg_info_sub_pg_info1_idx` (`pg_info_id`),
  CONSTRAINT `fk_pg_info_sub_pg_info1` FOREIGN KEY (`pg_info_id`) REFERENCES `pg_info` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=120 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int(10) unsigned NOT NULL COMMENT '등록 회원',
  `code` varchar(255) NOT NULL,
  `name` varchar(100) NOT NULL COMMENT '상품명',
  `type` varchar(16) DEFAULT NULL COMMENT '타입',
  `status` varchar(16) NOT NULL DEFAULT 'N' COMMENT '상태',
  `view_yn` varchar(1) DEFAULT NULL COMMENT '노출 여부',
  `view_start_date` datetime DEFAULT NULL COMMENT '노출 시작일',
  `view_end_date` datetime DEFAULT NULL COMMENT '노출 종료일',
  `summary` varchar(255) DEFAULT NULL COMMENT '간략 설명',
  `keyword` text DEFAULT NULL COMMENT '검색 키워드',
  `contents` text DEFAULT NULL COMMENT '상품 내용',
  `tax` varchar(8) DEFAULT NULL COMMENT '과세 여부',
  `min_purchase_limit` varchar(10) DEFAULT NULL COMMENT '최소 구매수량',
  `max_purchase_limit` varchar(10) DEFAULT NULL COMMENT '최대 구매수량',
  `adult` varchar(1) DEFAULT 'N' COMMENT '성인 인증 필요 여부',
  `hscode` varchar(16) DEFAULT NULL COMMENT '수출입코드',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `ipcc_yn` varchar(1) DEFAULT 'N' COMMENT '개인통관고유부호 사용 여부',
  `cancel_yn` varchar(1) DEFAULT 'Y' COMMENT '청약 철회 여부',
  `confirm` varchar(1) DEFAULT 'N' COMMENT '승인 여부',
  `video` varchar(255) DEFAULT NULL,
  `memo` text DEFAULT NULL,
  `common_info_id` int(10) unsigned DEFAULT NULL COMMENT '공통정보',
  `shipping_info_id` int(10) unsigned DEFAULT NULL COMMENT '배송정보',
  `writer_id` int(10) unsigned NOT NULL COMMENT '작성자',
  `inven_use` varchar(1) NOT NULL DEFAULT 'Y' COMMENT '재고 사용',
  `coupon_yn` varchar(1) DEFAULT 'Y' COMMENT '쿠폰 사용 여부',
  `option_use` varchar(1) DEFAULT 'N' COMMENT '옵션 사용 여부',
  `barcode` varchar(45) DEFAULT NULL,
  `user_limit` int(11) DEFAULT NULL COMMENT '1인당 구매횟수 제한',
  `use_end_period` int(11) DEFAULT NULL COMMENT '비실물 상품 사용 기한 (일)',
  `use_end_date` datetime DEFAULT NULL COMMENT '비실물 상품 사용 기한 (지정 일시)',
  `sale_start_date` datetime DEFAULT NULL COMMENT '판매 가능 시간 시작',
  `sale_end_date` datetime DEFAULT NULL COMMENT '판매 가능 시간 종료',
  `sale_start_time` time DEFAULT NULL COMMENT '판매 가능 일(시각) 시작',
  `sale_end_time` time DEFAULT NULL COMMENT '판매 가능 일(시각) 종료',
  `tel` varchar(16) DEFAULT NULL,
  `address` varchar(128) DEFAULT NULL,
  `address_detail` varchar(255) DEFAULT NULL,
  `lat` varchar(32) DEFAULT NULL,
  `lng` varchar(32) DEFAULT NULL,
  `subtitle` varchar(100) DEFAULT NULL COMMENT '부제목',
  `view_inventory` varchar(1) DEFAULT 'N' COMMENT '재고 노출여부',
  `view_end_time` varchar(1) DEFAULT 'N' COMMENT '판매 종료시간 노출여부',
  `reject` varchar(255) DEFAULT NULL COMMENT '반려 사유',
  `pg_provider` varchar(256) DEFAULT NULL COMMENT 'PG사 제외 선택, 구분자 |',
  `api_provider` varchar(64) DEFAULT NULL COMMENT '외부업체 연동 구분',
  `api_goods_id` text DEFAULT NULL COMMENT '외부업체 상품 ID',
  `use_place` text DEFAULT NULL COMMENT 'E쿠폰 사용처',
  `user_limit_reset` varchar(128) DEFAULT NULL COMMENT '1인당 구매횟수 제한 초기화 방법',
  `resale` varchar(2) DEFAULT 'N' COMMENT '사입 여부',
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_code_uindex` (`code`),
  KEY `fk_product_member1_idx` (`member_id`),
  KEY `fk_product_common_info1_idx` (`common_info_id`),
  KEY `fk_product_shipping_info1_idx` (`shipping_info_id`),
  KEY `fk_product_member2_idx` (`writer_id`),
  CONSTRAINT `fk_product_common_info1` FOREIGN KEY (`common_info_id`) REFERENCES `common_info` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_member2` FOREIGN KEY (`writer_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_shipping_info1` FOREIGN KEY (`shipping_info_id`) REFERENCES `shipping_info` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=503 DEFAULT CHARSET=utf8mb4 COMMENT='상품';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_add_option_group`
--

DROP TABLE IF EXISTS `product_add_option_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_add_option_group` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(10) unsigned NOT NULL,
  `add_option_group_id` int(10) unsigned NOT NULL,
  `sort` int(11) DEFAULT 99,
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_product_add_option_group` (`product_id`,`add_option_group_id`),
  KEY `fk_product_add_option_group_product1_idx` (`product_id`),
  KEY `fk_product_add_option_group_add_option_group1_idx` (`add_option_group_id`),
  CONSTRAINT `fk_product_add_option_group_add_option_group1` FOREIGN KEY (`add_option_group_id`) REFERENCES `add_option_group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_add_option_group_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='상품-추가옵션 연결';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_badge`
--

DROP TABLE IF EXISTS `product_badge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_badge` (
  `badge_id` int(11) NOT NULL,
  `product_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`badge_id`,`product_id`),
  KEY `fk_product_badge_badge1_idx` (`badge_id`),
  KEY `fk_product_badge_product1_idx` (`product_id`),
  CONSTRAINT `fk_product_badge_badge1` FOREIGN KEY (`badge_id`) REFERENCES `badge` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_badge_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='상품-뱃지 연결';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_brand`
--

DROP TABLE IF EXISTS `product_brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_brand` (
  `product_id` int(10) unsigned NOT NULL,
  `brand_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`product_id`,`brand_id`),
  UNIQUE KEY `u_product_brand` (`product_id`,`brand_id`),
  KEY `fk_product_brand_product1_idx` (`product_id`),
  KEY `fk_product_brand_brand1_idx` (`brand_id`),
  CONSTRAINT `fk_product_brand_brand1` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_brand_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='상품-브랜드 연결';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_category`
--

DROP TABLE IF EXISTS `product_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_category` (
  `product_id` int(10) unsigned NOT NULL,
  `category_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`product_id`,`category_id`),
  UNIQUE KEY `u_product_category` (`product_id`,`category_id`),
  KEY `fk_product_category_product1_idx` (`product_id`),
  KEY `fk_product_category_category1_idx` (`category_id`),
  CONSTRAINT `fk_product_category_category1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_product_category_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='상품-분류 연결';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_group`
--

DROP TABLE IF EXISTS `product_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_group` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `pid` int(10) unsigned NOT NULL COMMENT '그룹 상품',
  `product_id` int(10) unsigned NOT NULL COMMENT '대상 상품',
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_pid_product_id` (`pid`,`product_id`),
  KEY `fk_product_group_product1_idx` (`pid`),
  KEY `fk_product_group_product2_idx` (`product_id`),
  CONSTRAINT `fk_product_group_product1` FOREIGN KEY (`pid`) REFERENCES `product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_group_product2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_option`
--

DROP TABLE IF EXISTS `product_option`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_option` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(45) DEFAULT NULL COMMENT '코드',
  `supply_price` decimal(10,2) NOT NULL COMMENT '공급가',
  `origin_price` decimal(10,2) NOT NULL COMMENT '정상가',
  `selling_price` decimal(10,2) NOT NULL COMMENT '판매가',
  `view_yn` varchar(1) NOT NULL DEFAULT 'Y' COMMENT '노출 여부',
  `default_yn` varchar(45) NOT NULL DEFAULT 'N' COMMENT '기본 값 여부',
  `product_id` int(10) unsigned NOT NULL,
  `weight` decimal(5,2) DEFAULT NULL,
  `status` varchar(2) NOT NULL DEFAULT 'Y',
  `option_title` varchar(100) DEFAULT NULL,
  `option_1` varchar(100) DEFAULT NULL,
  `option_2` varchar(100) DEFAULT NULL,
  `option_3` varchar(100) DEFAULT NULL,
  `option_4` varchar(100) DEFAULT NULL,
  `option_5` varchar(100) DEFAULT NULL,
  `option_code_1` varchar(100) DEFAULT NULL,
  `option_code_2` varchar(100) DEFAULT NULL,
  `option_code_3` varchar(100) DEFAULT NULL,
  `option_code_4` varchar(100) DEFAULT NULL,
  `option_code_5` varchar(100) DEFAULT NULL,
  `option_tmp_price` varchar(100) DEFAULT NULL,
  `day_able_count` int(11) DEFAULT NULL COMMENT '일 처리가능수량',
  PRIMARY KEY (`id`),
  KEY `fk_product_option_product1_idx` (`product_id`),
  CONSTRAINT `fk_product_option_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2144 DEFAULT CHARSET=utf8mb4 COMMENT='상품 옵션';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_photo`
--

DROP TABLE IF EXISTS `product_photo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_photo` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(10) unsigned NOT NULL,
  `uri` varchar(256) DEFAULT NULL COMMENT 'URI',
  `reg_dt` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_dt` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `product_option_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_product_photo_product1_idx` (`product_id`),
  KEY `fk_product_photo_product_option1` (`product_option_id`),
  CONSTRAINT `fk_product_photo_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_product_photo_product_option1` FOREIGN KEY (`product_option_id`) REFERENCES `product_option` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=684 DEFAULT CHARSET=utf8mb4 COMMENT='상품 사진';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_qna`
--

DROP TABLE IF EXISTS `product_qna`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_qna` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL COMMENT '제목',
  `contents` text NOT NULL COMMENT '내용',
  `product_id` int(10) unsigned DEFAULT NULL,
  `status` varchar(2) DEFAULT 'Y' COMMENT '상태',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `product_qna_id` int(10) unsigned zerofill DEFAULT NULL COMMENT '답변일 경우 질문 product qna id',
  `admin_id` int(10) unsigned zerofill DEFAULT NULL,
  `a_member_id` int(10) unsigned zerofill DEFAULT NULL,
  `store_code` varchar(16) DEFAULT NULL,
  `secret` varchar(1) DEFAULT 'N',
  `customer_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_product_qna_product1_idx` (`product_id`),
  KEY `fk_product_qna_product_qna1_idx` (`product_qna_id`),
  KEY `fk_product_qna_member2_idx` (`a_member_id`),
  KEY `fk_product_qna_store1_idx` (`store_code`),
  KEY `fk_product_qna_customer1_idx` (`customer_id`),
  CONSTRAINT `fk_product_qna_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_qna_member2` FOREIGN KEY (`a_member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_qna_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_qna_product_qna1` FOREIGN KEY (`product_qna_id`) REFERENCES `product_qna` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_qna_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COMMENT='상품 문의';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_request`
--

DROP TABLE IF EXISTS `product_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_request` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int(10) unsigned NOT NULL,
  `store_code` varchar(16) NOT NULL,
  `title` varchar(100) NOT NULL,
  `memo` varchar(255) DEFAULT NULL,
  `status` varchar(2) NOT NULL DEFAULT 'R',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `manager` int(10) unsigned DEFAULT NULL COMMENT '담당자',
  PRIMARY KEY (`id`),
  KEY `fk_product_request_member1_idx` (`member_id`),
  KEY `fk_product_request_member2_idx` (`manager`),
  KEY `fk_product_request_store1_idx` (`store_code`),
  CONSTRAINT `fk_product_request_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_product_request_member2` FOREIGN KEY (`manager`) REFERENCES `member` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_product_request_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_request_prd`
--

DROP TABLE IF EXISTS `product_request_prd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_request_prd` (
  `product_request_id` int(10) unsigned NOT NULL,
  `product_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`product_request_id`,`product_id`),
  KEY `fk_product_request_prd_product_request1_idx` (`product_request_id`),
  KEY `fk_product_request_prd_product1_idx` (`product_id`),
  CONSTRAINT `fk_product_request_prd_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_request_prd_product_request1` FOREIGN KEY (`product_request_id`) REFERENCES `product_request` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='상품요청-상품 연결';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_review`
--

DROP TABLE IF EXISTS `product_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_review` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` int(10) unsigned NOT NULL,
  `title` varchar(128) DEFAULT NULL COMMENT '제목',
  `contents` text DEFAULT NULL COMMENT '내용',
  `rating` decimal(2,1) DEFAULT NULL COMMENT '별점',
  `status` varchar(2) DEFAULT 'Y' COMMENT '상태',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `order_info` varchar(255) DEFAULT NULL COMMENT '구매 관련 정보',
  `order_product_id` bigint(20) unsigned NOT NULL,
  `customer_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_product_review_product1_idx` (`product_id`),
  KEY `fk_product_review_order_product1_idx` (`order_product_id`),
  KEY `fk_product_review_customer1_idx` (`customer_id`),
  CONSTRAINT `fk_product_review_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_review_order_product1` FOREIGN KEY (`order_product_id`) REFERENCES `order_product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_review_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COMMENT='상품 리뷰';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_review_photo`
--

DROP TABLE IF EXISTS `product_review_photo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_review_photo` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_review_id` int(10) unsigned NOT NULL,
  `uri` varchar(256) DEFAULT NULL COMMENT 'URI',
  `reg_dt` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_dt` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `fk_product_review_photo_product_review1_idx` (`product_review_id`),
  CONSTRAINT `fk_product_review_photo_product_review1` FOREIGN KEY (`product_review_id`) REFERENCES `product_review` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COMMENT='상품 리뷰 사진';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_store_memo`
--

DROP TABLE IF EXISTS `product_store_memo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_store_memo` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `memo` text NOT NULL,
  `product_id` int(10) unsigned NOT NULL,
  `store_code` varchar(16) NOT NULL,
  `member_id` int(10) unsigned NOT NULL,
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_product_store_memo` (`product_id`,`store_code`),
  KEY `fk_product_store_memo_product1_idx` (`product_id`),
  KEY `fk_product_store_memo_store1_idx` (`store_code`),
  KEY `fk_product_store_memo_member1_idx` (`member_id`),
  CONSTRAINT `fk_product_store_memo_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_store_memo_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_store_memo_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=245 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `push_message`
--

DROP TABLE IF EXISTS `push_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `push_message` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `target` varchar(16) NOT NULL COMMENT 'A, I, T',
  `os` varchar(16) DEFAULT NULL,
  `save` varchar(2) DEFAULT 'Y' COMMENT '푸시 알림함 저장 여부',
  `status` varchar(2) DEFAULT 'Y',
  `title` varchar(128) DEFAULT NULL,
  `body` text DEFAULT NULL,
  `link` varchar(1024) DEFAULT NULL,
  `image` varchar(512) DEFAULT NULL,
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `res_date` datetime DEFAULT NULL COMMENT '예약일시',
  `can_date` datetime DEFAULT NULL COMMENT '취소일시',
  `customer_id` int(10) unsigned DEFAULT NULL,
  `store_code` varchar(16) DEFAULT NULL,
  `member_id` int(10) unsigned DEFAULT NULL COMMENT '등록자',
  PRIMARY KEY (`id`),
  KEY `fk_push_history_customer1_idx` (`customer_id`),
  KEY `fk_push_history_store1_idx` (`store_code`),
  KEY `fk_push_message_member1_idx` (`member_id`),
  CONSTRAINT `fk_push_history_customer10` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_push_history_store10` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_push_message_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `push_token`
--

DROP TABLE IF EXISTS `push_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `push_token` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `token` varchar(256) NOT NULL,
  `tester` varchar(2) DEFAULT 'N',
  `reg_date` datetime DEFAULT current_timestamp(),
  `app_info_id` int(11) NOT NULL,
  `customer_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_token_app_customer` (`token`,`app_info_id`,`customer_id`),
  KEY `fk_push_token_app_info1_idx` (`app_info_id`),
  KEY `fk_push_token_customer1_idx` (`customer_id`),
  CONSTRAINT `fk_push_token_app_info1` FOREIGN KEY (`app_info_id`) REFERENCES `app_info` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_push_token_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `qna`
--

DROP TABLE IF EXISTS `qna`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `qna` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(32) DEFAULT NULL COMMENT '문의유형',
  `title` varchar(128) NOT NULL COMMENT '제목',
  `contents` text NOT NULL COMMENT '내용',
  `q_member_id` int(10) unsigned NOT NULL COMMENT '질문자',
  `status` varchar(2) DEFAULT NULL COMMENT '상태',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `qna_id` int(10) unsigned DEFAULT NULL COMMENT '답변일 경우 질문 qna id',
  `admin_id` int(10) unsigned DEFAULT NULL,
  `a_member_id` int(10) unsigned DEFAULT NULL,
  `store_code` varchar(16) DEFAULT NULL,
  `secret` varchar(1) DEFAULT 'N',
  PRIMARY KEY (`id`),
  KEY `fk_qna_member1_idx` (`q_member_id`),
  KEY `fk_qna_qna1_idx` (`qna_id`),
  KEY `fk_qna_member2_idx` (`a_member_id`),
  KEY `fk_qna_store1_idx` (`store_code`),
  CONSTRAINT `fk_qna_member1` FOREIGN KEY (`q_member_id`) REFERENCES `member` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_qna_member2` FOREIGN KEY (`a_member_id`) REFERENCES `member` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_qna_qna1` FOREIGN KEY (`qna_id`) REFERENCES `qna` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_qna_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COMMENT='문의';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `qna_store`
--

DROP TABLE IF EXISTS `qna_store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `qna_store` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(32) DEFAULT NULL COMMENT '문의유형',
  `title` varchar(128) NOT NULL COMMENT '제목',
  `contents` text NOT NULL COMMENT '내용',
  `status` varchar(2) DEFAULT NULL COMMENT '상태',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `qna_id` int(10) unsigned DEFAULT NULL COMMENT '답변일 경우 질문 qna id',
  `admin_id` int(10) unsigned DEFAULT NULL,
  `a_member_id` int(10) unsigned DEFAULT NULL,
  `store_code` varchar(16) DEFAULT NULL,
  `secret` varchar(1) DEFAULT 'N',
  `customer_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_qna_qna1_idx` (`qna_id`),
  KEY `fk_qna_member2_idx` (`a_member_id`),
  KEY `fk_qna_store1_idx` (`store_code`),
  KEY `fk_qna_store_customer1_idx` (`customer_id`),
  CONSTRAINT `fk_qna_member20` FOREIGN KEY (`a_member_id`) REFERENCES `member` (`id`) ON DELETE SET NULL ON UPDATE NO ACTION,
  CONSTRAINT `fk_qna_qna10` FOREIGN KEY (`qna_id`) REFERENCES `qna_store` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_qna_store10` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_qna_store_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COMMENT='문의 (상점)';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `revenue_offline`
--

DROP TABLE IF EXISTS `revenue_offline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `revenue_offline` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(100) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `sales_date` datetime NOT NULL,
  `status` varchar(2) NOT NULL DEFAULT 'Y',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `member_id` int(10) unsigned DEFAULT NULL COMMENT '등록자',
  PRIMARY KEY (`id`),
  KEY `revenue_offline_member_id_fk` (`member_id`),
  CONSTRAINT `revenue_offline_member_id_fk` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2381 DEFAULT CHARSET=utf8mb4 COMMENT='오프라인 매출';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rural_postcode`
--

DROP TABLE IF EXISTS `rural_postcode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rural_postcode` (
  `post_code` int(11) NOT NULL,
  `area` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`post_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='도서산간 우편번호';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `setting_value`
--

DROP TABLE IF EXISTS `setting_value`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `setting_value` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(32) DEFAULT NULL COMMENT '타입',
  `name` varchar(64) DEFAULT NULL COMMENT '이름',
  `value` text DEFAULT NULL COMMENT '값',
  `description` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COMMENT='설정 값';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `settlement_data`
--

DROP TABLE IF EXISTS `settlement_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `settlement_data` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `target_date` date NOT NULL,
  `account_raw_id` int(10) unsigned NOT NULL,
  `member_id` int(10) unsigned NOT NULL,
  `type` varchar(3) NOT NULL COMMENT 'S(공급가), C(수수료)',
  `sequence` int(11) NOT NULL COMMENT '정산 순번',
  `target_amount` decimal(10,2) NOT NULL COMMENT '정산 대상 금액',
  `amount` decimal(10,2) NOT NULL COMMENT '정산 금액',
  `commission_type` varchar(2) DEFAULT NULL,
  `commission_value` decimal(10,2) DEFAULT NULL,
  `payment_date` datetime DEFAULT NULL COMMENT '정산 지급일',
  `reg_date` datetime DEFAULT current_timestamp(),
  `pg_provider` varchar(16) DEFAULT NULL,
  `pg_kind` varchar(16) DEFAULT NULL,
  `status` varchar(2) DEFAULT 'R' COMMENT '상태',
  `reject` varchar(255) DEFAULT NULL COMMENT '반려 사유',
  `tax` varchar(1) DEFAULT NULL,
  `payment` varchar(2) DEFAULT NULL COMMENT '지급 방식',
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `fk_account_data_account_raw1_idx` (`account_raw_id`),
  KEY `fk_account_data_member1_idx` (`member_id`),
  CONSTRAINT `fk_account_data_account_raw1` FOREIGN KEY (`account_raw_id`) REFERENCES `settlement_raw` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_account_data_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1301 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `settlement_excel`
--

DROP TABLE IF EXISTS `settlement_excel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `settlement_excel` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int(10) unsigned NOT NULL,
  `member_type` varchar(16) DEFAULT NULL,
  `target_kind` varchar(16) DEFAULT NULL,
  `target_status` varchar(2) DEFAULT NULL,
  `s_reg_date` date DEFAULT NULL,
  `e_reg_date` date DEFAULT NULL,
  `request_member` int(10) unsigned NOT NULL,
  `status` varchar(2) DEFAULT NULL,
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `file` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_settlement_excel_member1_idx` (`member_id`),
  KEY `fk_settlement_excel_member2_idx` (`request_member`),
  CONSTRAINT `fk_settlement_excel_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_settlement_excel_member2` FOREIGN KEY (`request_member`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COMMENT='정산 내역 엑셀 요청';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `settlement_raw`
--

DROP TABLE IF EXISTS `settlement_raw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `settlement_raw` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `target_date` date NOT NULL,
  `order_id` bigint(20) NOT NULL,
  `order_product_id` bigint(20) unsigned NOT NULL,
  `store_code` varchar(16) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `pg_type` varchar(45) NOT NULL,
  `supply_price` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT '공급가',
  `margin_price` decimal(10,2) NOT NULL DEFAULT 0.00 COMMENT '마진가',
  `processed` datetime DEFAULT NULL,
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `product_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_settlement_raw_product1_idx` (`product_id`),
  KEY `settlement_raw_order_product_id_fk` (`order_product_id`),
  KEY `settlement_raw_store_code_fk` (`store_code`),
  CONSTRAINT `fk_settlement_raw_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `settlement_raw_order_product_id_fk` FOREIGN KEY (`order_product_id`) REFERENCES `order_product` (`id`),
  CONSTRAINT `settlement_raw_store_code_fk` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=270 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `settlement_ship`
--

DROP TABLE IF EXISTS `settlement_ship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `settlement_ship` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `target_date` date NOT NULL,
  `order_id` bigint(20) NOT NULL,
  `order_shipping_id` bigint(20) NOT NULL,
  `store_code` varchar(16) NOT NULL,
  `type` varchar(2) NOT NULL COMMENT 'S(공급가), C(수수료)',
  `sequence` int(11) NOT NULL COMMENT '정산 순번',
  `target_amount` decimal(10,2) NOT NULL COMMENT '정산 대상 금액',
  `amount` decimal(10,2) NOT NULL COMMENT '정산 금액',
  `member_id` int(10) unsigned NOT NULL,
  `payment_date` datetime DEFAULT NULL COMMENT '정산 지급일',
  `reg_date` datetime DEFAULT current_timestamp(),
  `commission_type` varchar(2) DEFAULT NULL,
  `commission_value` decimal(10,2) DEFAULT NULL,
  `pg_provider` varchar(16) DEFAULT NULL,
  `pg_kind` varchar(16) DEFAULT NULL,
  `status` varchar(2) DEFAULT 'R' COMMENT '상태',
  `reject` varchar(255) DEFAULT NULL COMMENT '반려 사유',
  `mod_date` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `fk_settlement_ship_member1_idx` (`member_id`),
  KEY `settlement_ship_store_code_fk` (`store_code`),
  CONSTRAINT `fk_settlement_ship_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `settlement_ship_store_code_fk` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=261 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shipping_area`
--

DROP TABLE IF EXISTS `shipping_area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipping_area` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL COMMENT '이름',
  `cost` int(11) NOT NULL COMMENT '비용',
  `shipping_cost_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_shipping_area_shipping_cost1_idx` (`shipping_cost_id`),
  CONSTRAINT `fk_shipping_area_shipping_cost1` FOREIGN KEY (`shipping_cost_id`) REFERENCES `shipping_cost` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='배송지역';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shipping_area_detail`
--

DROP TABLE IF EXISTS `shipping_area_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipping_area_detail` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `category_text` varchar(128) DEFAULT NULL COMMENT '계층구조 풀 텍스트',
  `zipcode` varchar(45) DEFAULT NULL COMMENT '우편번호',
  `address_house` varchar(64) DEFAULT NULL COMMENT '지번 주소',
  `address_street` varchar(64) DEFAULT NULL COMMENT '도로명 주소',
  `shipping_area_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_shipping_area_detail_shipping_area1_idx` (`shipping_area_id`),
  CONSTRAINT `fk_shipping_area_detail_shipping_area1` FOREIGN KEY (`shipping_area_id`) REFERENCES `shipping_area` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='배송지역 상세';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shipping_cost`
--

DROP TABLE IF EXISTS `shipping_cost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipping_cost` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(10) DEFAULT NULL COMMENT '배송비 타입 free, fix, cost, ea, weight',
  `category` varchar(16) DEFAULT NULL COMMENT 'basic(기본), add(추가)',
  `cost` int(11) NOT NULL DEFAULT 0 COMMENT '비용',
  `section_start` int(11) DEFAULT NULL COMMENT '구간시작',
  `section_end` int(11) DEFAULT NULL COMMENT '구간끝',
  `section_repeat` int(11) DEFAULT NULL COMMENT '구간 반복',
  `shipping_info_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_shipping_cost_shipping_info1_idx` (`shipping_info_id`),
  CONSTRAINT `fk_shipping_cost_shipping_info1` FOREIGN KEY (`shipping_info_id`) REFERENCES `shipping_info` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=369 DEFAULT CHARSET=utf8mb4 COMMENT='배송 금액';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shipping_info`
--

DROP TABLE IF EXISTS `shipping_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipping_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL COMMENT '이름',
  `type` varchar(10) NOT NULL COMMENT '배송방법 (택배,퀵서비스,화물배송,매장수령)',
  `pay_type` varchar(10) NOT NULL COMMENT '지불방법 (선불,착불)',
  `calc_type` varchar(10) NOT NULL COMMENT '계산타입 [묶음계산-묶음배송/개별계산-개별배송 /무료계산-묶음배송]',
  `return_cost` int(11) DEFAULT 0 COMMENT '반품비',
  `change_cost` int(11) DEFAULT 0 COMMENT '교환비',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `status` varchar(2) NOT NULL DEFAULT 'Y',
  `member_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_shipping_info_member1_idx` (`member_id`),
  CONSTRAINT `fk_shipping_info_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COMMENT='배송 정보';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shipping_tracking`
--

DROP TABLE IF EXISTS `shipping_tracking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipping_tracking` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `location` varchar(45) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `msg` varchar(128) NOT NULL,
  `agent` varchar(16) DEFAULT NULL,
  `tel` varchar(16) DEFAULT NULL,
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `order_shipping_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_shipping_tracking_order_shipping1_idx` (`order_shipping_id`),
  CONSTRAINT `fk_shipping_tracking_order_shipping1` FOREIGN KEY (`order_shipping_id`) REFERENCES `order_shipping` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='배송 추적 상세';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shop`
--

DROP TABLE IF EXISTS `shop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` text NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `address_detail` varchar(255) DEFAULT NULL,
  `work_time` varchar(512) DEFAULT NULL COMMENT '운영시간',
  `holiday` varchar(128) DEFAULT NULL COMMENT '휴무일',
  `image` varchar(512) DEFAULT NULL,
  `lat` varchar(45) DEFAULT NULL,
  `lng` varchar(45) DEFAULT NULL,
  `tel` varchar(45) DEFAULT NULL,
  `subtitle` varchar(100) DEFAULT NULL,
  `member_id` int(10) unsigned NOT NULL,
  `reg_date` datetime DEFAULT current_timestamp(),
  `mod_date` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `able_loc` text DEFAULT NULL,
  `order_type` varchar(12) DEFAULT NULL,
  `min_order_price` int(11) DEFAULT NULL,
  `origin` text DEFAULT NULL,
  `confirm_pass` varchar(16) DEFAULT NULL,
  `status` varchar(3) DEFAULT NULL,
  `sort` int(11) DEFAULT 99,
  `transfer_id` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_shop_member1_idx` (`member_id`),
  CONSTRAINT `fk_shop_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COMMENT='매장';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shop_badge`
--

DROP TABLE IF EXISTS `shop_badge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop_badge` (
  `shop_id` int(10) unsigned NOT NULL,
  `badge_id` int(11) NOT NULL,
  PRIMARY KEY (`shop_id`,`badge_id`),
  KEY `fk_shop_badge_shop1_idx` (`shop_id`),
  KEY `fk_shop_badge_badge1_idx` (`badge_id`),
  CONSTRAINT `fk_shop_badge_badge1` FOREIGN KEY (`badge_id`) REFERENCES `badge` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_shop_badge_shop1` FOREIGN KEY (`shop_id`) REFERENCES `shop` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='매장-뱃지 연결';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shop_category`
--

DROP TABLE IF EXISTS `shop_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `image` varchar(512) NOT NULL,
  `status` varchar(2) NOT NULL DEFAULT 'N',
  `sort` int(11) DEFAULT 99,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='매장 분류';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shop_photo`
--

DROP TABLE IF EXISTS `shop_photo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop_photo` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `uri` varchar(512) NOT NULL,
  `shop_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_shop_photo_shop1_idx` (`shop_id`),
  CONSTRAINT `fk_shop_photo_shop1` FOREIGN KEY (`shop_id`) REFERENCES `shop` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='매장 이미지';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shop_shop_category`
--

DROP TABLE IF EXISTS `shop_shop_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop_shop_category` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `shop_category_id` int(11) NOT NULL,
  `shop_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_shop_shop_category` (`shop_category_id`,`shop_id`),
  KEY `fk_shop_shop_category_shop_category1_idx` (`shop_category_id`),
  KEY `fk_shop_shop_category_shop1_idx` (`shop_id`),
  CONSTRAINT `fk_shop_shop_category_shop1` FOREIGN KEY (`shop_id`) REFERENCES `shop` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_shop_shop_category_shop_category1` FOREIGN KEY (`shop_category_id`) REFERENCES `shop_category` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='매장-매장분류 연결';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shop_tab`
--

DROP TABLE IF EXISTS `shop_tab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop_tab` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `status` varchar(2) NOT NULL DEFAULT 'N',
  `sort` int(11) NOT NULL DEFAULT 99,
  `reg_date` datetime DEFAULT current_timestamp(),
  `mod_date` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `shop_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_shop_tab_shop1_idx` (`shop_id`),
  CONSTRAINT `fk_shop_tab_shop1` FOREIGN KEY (`shop_id`) REFERENCES `shop` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='매장 메뉴 탭';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shop_tab_product`
--

DROP TABLE IF EXISTS `shop_tab_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shop_tab_product` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `shop_tab_id` int(10) unsigned NOT NULL,
  `product_id` int(10) unsigned NOT NULL,
  `sort` int(11) DEFAULT 99,
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_shop_tab_product` (`shop_tab_id`,`product_id`),
  KEY `fk_shop_tab_product_shop_tab1_idx` (`shop_tab_id`),
  KEY `fk_shop_tab_product_product1_idx` (`product_id`),
  CONSTRAINT `fk_shop_tab_product_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_shop_tab_product_shop_tab1` FOREIGN KEY (`shop_tab_id`) REFERENCES `shop_tab` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='매장 탭-상품 연결';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_history`
--

DROP TABLE IF EXISTS `sms_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_history` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(16) DEFAULT NULL COMMENT '타입',
  `mobile` varchar(128) DEFAULT NULL COMMENT '휴대전화',
  `title` varchar(32) DEFAULT NULL COMMENT '제목',
  `body` text DEFAULT NULL COMMENT '내용',
  `status` varchar(2) DEFAULT NULL COMMENT '상태',
  `mid` varchar(32) DEFAULT NULL COMMENT '전송결과 id',
  `provider` varchar(16) DEFAULT NULL COMMENT '제공 업체',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `res_date` datetime DEFAULT NULL COMMENT '예약일시',
  `can_date` datetime DEFAULT NULL COMMENT '취소일시',
  `member_id` int(10) unsigned DEFAULT NULL,
  `customer_id` int(10) unsigned DEFAULT NULL,
  `order_id` bigint(20) unsigned DEFAULT NULL,
  `store_code` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_sms_history_member1_idx` (`member_id`),
  KEY `fk_sms_history_order1_idx` (`order_id`),
  KEY `fk_sms_history_store1_idx` (`store_code`),
  KEY `fk_sms_history_customer1_idx` (`customer_id`),
  CONSTRAINT `fk_sms_history_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_sms_history_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_sms_history_order1` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_sms_history_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=286 DEFAULT CHARSET=utf8mb4 COMMENT='SMS 전송 기록';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `store`
--

DROP TABLE IF EXISTS `store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store` (
  `code` varchar(16) NOT NULL,
  `member_id` int(10) unsigned NOT NULL COMMENT '상점 생성 회원',
  `title` varchar(45) DEFAULT NULL COMMENT '상점명',
  `type` varchar(2) DEFAULT NULL COMMENT '폐쇄몰 오픈몰',
  `domain` varchar(128) DEFAULT NULL,
  `status` varchar(2) NOT NULL DEFAULT 'R',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `layout` text DEFAULT NULL,
  `auto_join` varchar(2) NOT NULL DEFAULT 'Y' COMMENT '회원가입 자동승인',
  `logo_pc` varchar(512) DEFAULT NULL,
  `logo_mobile` varchar(512) DEFAULT NULL,
  `favicon` varchar(512) DEFAULT NULL,
  `info` text DEFAULT NULL,
  `dupl_store` varchar(16) DEFAULT NULL COMMENT '복제 대상 상점 코드',
  `able_target_use` varchar(1) NOT NULL DEFAULT 'N',
  `value` varchar(45) DEFAULT NULL,
  `verify_code` varchar(32) DEFAULT NULL COMMENT '가입방식 고정일때 사용하는 가입 검증 코드',
  `exclude_menu` text DEFAULT NULL COMMENT '상점에서 보이지 않을 메뉴 , split',
  `group` varchar(32) DEFAULT NULL,
  `prd_pg_opt_use` varchar(2) DEFAULT 'N' COMMENT '상품 PG 옵션 사용 여부',
  `meal_opt_use` varchar(2) DEFAULT 'N' COMMENT '식권 결제 옵션 사용 여부',
  `meal_opt_limit_use` varchar(2) DEFAULT 'N' COMMENT '식권 결제 사용시간 제한 사용 여부',
  `meal_opt_limit_time` varchar(512) DEFAULT '[]' COMMENT '식권 결제 사용시간 제한 시간 정보',
  `meal_opt_cancel_use` varchar(2) DEFAULT 'N' COMMENT '식권 결제 일괄 취소 기능 사용 여부',
  `keyword` text DEFAULT NULL,
  `copy_setting` varchar(16) DEFAULT NULL COMMENT '설정 복사 대상 상점코드',
  PRIMARY KEY (`code`),
  KEY `fk_mall_member1_idx` (`member_id`),
  CONSTRAINT `fk_mall_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='상점';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `store_board`
--

DROP TABLE IF EXISTS `store_board`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store_board` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL COMMENT '제목',
  `contents` text NOT NULL COMMENT '내용',
  `pin` varchar(1) DEFAULT 'N' COMMENT '상위 고정',
  `sort` int(11) DEFAULT 99 COMMENT '순서',
  `status` varchar(2) NOT NULL DEFAULT 'Y' COMMENT '상태',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `image` varchar(512) DEFAULT NULL,
  `view_start_date` datetime DEFAULT NULL COMMENT '노출 시작일',
  `view_end_date` datetime DEFAULT NULL COMMENT '노출 종료일',
  `start_date` datetime DEFAULT NULL COMMENT '\n시작일',
  `end_date` datetime DEFAULT NULL COMMENT '종료일',
  `store_board_group_id` int(10) unsigned DEFAULT NULL,
  `member_id` int(10) unsigned DEFAULT NULL,
  `customer_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_store_board_store_board_group1_idx` (`store_board_group_id`),
  KEY `fk_store_board_member1_idx` (`member_id`),
  KEY `fk_store_board_customer1_idx` (`customer_id`),
  CONSTRAINT `fk_store_board_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_store_board_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_store_board_store_board_group1` FOREIGN KEY (`store_board_group_id`) REFERENCES `store_board_group` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4 COMMENT='공지사항';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `store_board_cmt`
--

DROP TABLE IF EXISTS `store_board_cmt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store_board_cmt` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `comment` varchar(255) NOT NULL,
  `status` varchar(2) NOT NULL DEFAULT 'Y' COMMENT '상태',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `store_board_id` int(10) unsigned NOT NULL,
  `member_id` int(10) unsigned DEFAULT NULL,
  `customer_id` int(10) unsigned DEFAULT NULL,
  `p_id` int(10) unsigned DEFAULT NULL,
  `store_code` varchar(16) DEFAULT NULL COMMENT '작성된 상점',
  `ip` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_store_board_cmt_store_board1_idx` (`store_board_id`),
  KEY `fk_store_board_cmt_member1_idx` (`member_id`),
  KEY `fk_store_board_cmt_customer1_idx` (`customer_id`),
  KEY `fk_store_board_cmt_store_board_cmt1_idx` (`p_id`),
  KEY `store_board_cmt_store_code_fk` (`store_code`),
  CONSTRAINT `fk_store_board_cmt_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_store_board_cmt_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_store_board_cmt_store_board1` FOREIGN KEY (`store_board_id`) REFERENCES `store_board` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_store_board_cmt_store_board_cmt1` FOREIGN KEY (`p_id`) REFERENCES `store_board_cmt` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `store_board_cmt_store_code_fk` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COMMENT='상점 게시판 댓글';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `store_board_group`
--

DROP TABLE IF EXISTS `store_board_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store_board_group` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `menu_visible` varchar(2) NOT NULL DEFAULT 'N',
  `view_type` varchar(16) NOT NULL DEFAULT 'thumbnail' COMMENT 'thumbnail, banner',
  `view_end_content` varchar(1) DEFAULT 'N' COMMENT '기간 지난 컨텐츠 노출 여부',
  `status` varchar(2) NOT NULL DEFAULT 'Y' COMMENT '상태',
  `sort` int(11) DEFAULT 99 COMMENT '순서',
  `store_code` varchar(16) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_store_board_group_store1_idx` (`store_code`),
  CONSTRAINT `fk_store_board_group_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `store_popup`
--

DROP TABLE IF EXISTS `store_popup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store_popup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `store_code` varchar(16) NOT NULL,
  `title` varchar(45) NOT NULL,
  `contents` text DEFAULT NULL,
  `img` varchar(512) DEFAULT NULL,
  `link` varchar(512) DEFAULT NULL,
  `type` varchar(3) DEFAULT NULL,
  `status` varchar(2) NOT NULL DEFAULT 'N',
  `view_start_date` datetime DEFAULT NULL COMMENT '노출 시작일',
  `view_end_date` datetime DEFAULT NULL COMMENT '노출 종료일',
  `duplicate` varchar(1) DEFAULT 'N' COMMENT '복제상점에서 보여질지 여부',
  `sort` int(11) DEFAULT 99,
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `fk_store_popup_store1_idx` (`store_code`),
  CONSTRAINT `fk_store_popup_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `store_product`
--

DROP TABLE IF EXISTS `store_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store_product` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `store_code` varchar(16) NOT NULL,
  `product_id` int(10) unsigned NOT NULL,
  `view_yn` varchar(1) NOT NULL DEFAULT 'Y',
  `variation` int(11) NOT NULL DEFAULT 0 COMMENT '가격 변동값',
  `catalog_id` int(11) DEFAULT NULL COMMENT '카탈로그 출처',
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_store_product` (`store_code`,`product_id`),
  KEY `fk_store_product_store1_idx` (`store_code`),
  KEY `fk_store_product_product1_idx` (`product_id`),
  CONSTRAINT `fk_store_product_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_store_product_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2069 DEFAULT CHARSET=utf8mb4 COMMENT='상점-상품 연결';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `store_theme`
--

DROP TABLE IF EXISTS `store_theme`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store_theme` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` varchar(255) NOT NULL,
  `store_code` varchar(16) NOT NULL,
  `pid` int(10) unsigned DEFAULT NULL,
  `status` varchar(2) NOT NULL DEFAULT 'N',
  `reg_date` datetime NOT NULL DEFAULT current_timestamp(),
  `mod_date` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `layout` text DEFAULT NULL,
  `visible` varchar(2) DEFAULT 'Y' COMMENT '노출 여부',
  `top_visible` varchar(2) NOT NULL DEFAULT 'N',
  `use_layout` varchar(2) DEFAULT 'N',
  `sort` int(11) DEFAULT 99,
  PRIMARY KEY (`id`),
  KEY `fk_store_theme_store1_idx` (`store_code`),
  KEY `fk_store_theme_store_theme1_idx` (`pid`),
  CONSTRAINT `fk_store_theme_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE CASCADE,
  CONSTRAINT `fk_store_theme_store_theme1` FOREIGN KEY (`pid`) REFERENCES `store_theme` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=390 DEFAULT CHARSET=utf8mb4 COMMENT='상점 테마(상품 분류)';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `store_theme_product`
--

DROP TABLE IF EXISTS `store_theme_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store_theme_product` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `store_theme_id` int(10) unsigned NOT NULL,
  `product_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_store_theme_product` (`store_theme_id`,`product_id`),
  KEY `fk_store_theme_product_store_theme1_idx` (`store_theme_id`),
  KEY `fk_store_theme_product_product1_idx` (`product_id`),
  CONSTRAINT `fk_store_theme_product_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_store_theme_product_store_theme1` FOREIGN KEY (`store_theme_id`) REFERENCES `store_theme` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1323 DEFAULT CHARSET=utf8mb4 COMMENT='상점 테마 상품';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `store_theme_shop`
--

DROP TABLE IF EXISTS `store_theme_shop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store_theme_shop` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `store_theme_id` int(10) unsigned NOT NULL,
  `shop_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_store_theme_shop_store_theme1_idx` (`store_theme_id`),
  KEY `fk_store_theme_shop_shop1_idx` (`shop_id`),
  CONSTRAINT `fk_store_theme_shop_shop1` FOREIGN KEY (`shop_id`) REFERENCES `shop` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_store_theme_shop_store_theme1` FOREIGN KEY (`store_theme_id`) REFERENCES `store_theme` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=176 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sub_commission`
--

DROP TABLE IF EXISTS `sub_commission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sub_commission` (
  `id` bigint(20) unsigned NOT NULL,
  `type` varchar(2) NOT NULL COMMENT '퍼센트(P) or 고정(F)',
  `value` decimal(10,2) NOT NULL COMMENT '수수료',
  `commission_id` bigint(20) unsigned DEFAULT NULL,
  `sub_commission_id` bigint(20) unsigned DEFAULT NULL,
  `member_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_sub_commission_commission1_idx` (`commission_id`),
  KEY `fk_sub_commission_sub_commission1_idx` (`sub_commission_id`),
  KEY `fk_sub_commission_member1_idx` (`member_id`),
  CONSTRAINT `fk_sub_commission_commission1` FOREIGN KEY (`commission_id`) REFERENCES `commission` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_sub_commission_member1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_sub_commission_sub_commission1` FOREIGN KEY (`sub_commission_id`) REFERENCES `sub_commission` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wish_product`
--

DROP TABLE IF EXISTS `wish_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wish_product` (
  `product_id` int(10) unsigned NOT NULL,
  `customer_id` int(10) unsigned NOT NULL,
  `reg_date` datetime DEFAULT current_timestamp(),
  `store_code` varchar(16) NOT NULL,
  PRIMARY KEY (`product_id`,`customer_id`,`store_code`),
  KEY `fk_wish_product_product1_idx` (`product_id`),
  KEY `fk_wish_product_customer1_idx` (`customer_id`),
  KEY `fk_wish_product_store1_idx` (`store_code`),
  CONSTRAINT `fk_wish_product_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_wish_product_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_wish_product_store1` FOREIGN KEY (`store_code`) REFERENCES `store` (`code`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='관심 상품';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-04 15:49:35
