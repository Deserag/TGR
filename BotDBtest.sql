PGDMP     4    /                {         	   BotDBtest    15.2    15.2 $    (           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            )           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            *           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            +           1262    16696 	   BotDBtest    DATABASE        CREATE DATABASE "BotDBtest" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE "BotDBtest";
                postgres    false            �            1259    16768 
   classrooms    TABLE     y   CREATE TABLE public.classrooms (
    classroom_id integer NOT NULL,
    classroom_name character varying(50) NOT NULL
);
    DROP TABLE public.classrooms;
       public         heap    postgres    false            �            1259    16767    classrooms_classroom_id_seq    SEQUENCE     �   CREATE SEQUENCE public.classrooms_classroom_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.classrooms_classroom_id_seq;
       public          postgres    false    223            ,           0    0    classrooms_classroom_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.classrooms_classroom_id_seq OWNED BY public.classrooms.classroom_id;
          public          postgres    false    222            �            1259    16740    days    TABLE     g   CREATE TABLE public.days (
    day_id integer NOT NULL,
    day_name character varying(20) NOT NULL
);
    DROP TABLE public.days;
       public         heap    postgres    false            �            1259    16739    days_day_id_seq    SEQUENCE     �   CREATE SEQUENCE public.days_day_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.days_day_id_seq;
       public          postgres    false    215            -           0    0    days_day_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.days_day_id_seq OWNED BY public.days.day_id;
          public          postgres    false    214            �            1259    16747    groups    TABLE     m   CREATE TABLE public.groups (
    group_id integer NOT NULL,
    group_name character varying(50) NOT NULL
);
    DROP TABLE public.groups;
       public         heap    postgres    false            �            1259    16746    groups_group_id_seq    SEQUENCE     �   CREATE SEQUENCE public.groups_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.groups_group_id_seq;
       public          postgres    false    217            .           0    0    groups_group_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.groups_group_id_seq OWNED BY public.groups.group_id;
          public          postgres    false    216            �            1259    16775    lecture    TABLE     B  CREATE TABLE public.lecture (
    id_lecture integer NOT NULL,
    day character varying(50),
    subject character varying(100),
    teacher character varying(100),
    classroom character varying(50),
    group_id character varying(50),
    lecture_type character varying(100),
    lecture_time character varying(50)
);
    DROP TABLE public.lecture;
       public         heap    postgres    false            �            1259    16774    lecture_id_lecture_seq    SEQUENCE     �   CREATE SEQUENCE public.lecture_id_lecture_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.lecture_id_lecture_seq;
       public          postgres    false    225            /           0    0    lecture_id_lecture_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.lecture_id_lecture_seq OWNED BY public.lecture.id_lecture;
          public          postgres    false    224            �            1259    16754    subjects    TABLE     s   CREATE TABLE public.subjects (
    subject_id integer NOT NULL,
    subject_name character varying(50) NOT NULL
);
    DROP TABLE public.subjects;
       public         heap    postgres    false            �            1259    16753    subjects_subject_id_seq    SEQUENCE     �   CREATE SEQUENCE public.subjects_subject_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.subjects_subject_id_seq;
       public          postgres    false    219            0           0    0    subjects_subject_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.subjects_subject_id_seq OWNED BY public.subjects.subject_id;
          public          postgres    false    218            �            1259    16761    teachers    TABLE     �   CREATE TABLE public.teachers (
    teacher_id integer NOT NULL,
    teacher_name character varying(50) NOT NULL,
    teacher_midname character varying(50) NOT NULL,
    teacher_lastname character varying(50) NOT NULL
);
    DROP TABLE public.teachers;
       public         heap    postgres    false            �            1259    16760    teachers_teacher_id_seq    SEQUENCE     �   CREATE SEQUENCE public.teachers_teacher_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.teachers_teacher_id_seq;
       public          postgres    false    221            1           0    0    teachers_teacher_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.teachers_teacher_id_seq OWNED BY public.teachers.teacher_id;
          public          postgres    false    220            �            1259    16991    users    TABLE     �   CREATE TABLE public.users (
    telegram_id character varying(100) NOT NULL,
    user_group character varying(100),
    user_admin boolean DEFAULT false,
    user_mail boolean DEFAULT false
);
    DROP TABLE public.users;
       public         heap    postgres    false            �           2604    16771    classrooms classroom_id    DEFAULT     �   ALTER TABLE ONLY public.classrooms ALTER COLUMN classroom_id SET DEFAULT nextval('public.classrooms_classroom_id_seq'::regclass);
 F   ALTER TABLE public.classrooms ALTER COLUMN classroom_id DROP DEFAULT;
       public          postgres    false    223    222    223            �           2604    16743    days day_id    DEFAULT     j   ALTER TABLE ONLY public.days ALTER COLUMN day_id SET DEFAULT nextval('public.days_day_id_seq'::regclass);
 :   ALTER TABLE public.days ALTER COLUMN day_id DROP DEFAULT;
       public          postgres    false    215    214    215            �           2604    16750    groups group_id    DEFAULT     r   ALTER TABLE ONLY public.groups ALTER COLUMN group_id SET DEFAULT nextval('public.groups_group_id_seq'::regclass);
 >   ALTER TABLE public.groups ALTER COLUMN group_id DROP DEFAULT;
       public          postgres    false    217    216    217            �           2604    16778    lecture id_lecture    DEFAULT     x   ALTER TABLE ONLY public.lecture ALTER COLUMN id_lecture SET DEFAULT nextval('public.lecture_id_lecture_seq'::regclass);
 A   ALTER TABLE public.lecture ALTER COLUMN id_lecture DROP DEFAULT;
       public          postgres    false    224    225    225            �           2604    16757    subjects subject_id    DEFAULT     z   ALTER TABLE ONLY public.subjects ALTER COLUMN subject_id SET DEFAULT nextval('public.subjects_subject_id_seq'::regclass);
 B   ALTER TABLE public.subjects ALTER COLUMN subject_id DROP DEFAULT;
       public          postgres    false    219    218    219            �           2604    16764    teachers teacher_id    DEFAULT     z   ALTER TABLE ONLY public.teachers ALTER COLUMN teacher_id SET DEFAULT nextval('public.teachers_teacher_id_seq'::regclass);
 B   ALTER TABLE public.teachers ALTER COLUMN teacher_id DROP DEFAULT;
       public          postgres    false    221    220    221            �           2606    16773    classrooms classrooms_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.classrooms
    ADD CONSTRAINT classrooms_pkey PRIMARY KEY (classroom_id);
 D   ALTER TABLE ONLY public.classrooms DROP CONSTRAINT classrooms_pkey;
       public            postgres    false    223            �           2606    16745    days days_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.days
    ADD CONSTRAINT days_pkey PRIMARY KEY (day_id);
 8   ALTER TABLE ONLY public.days DROP CONSTRAINT days_pkey;
       public            postgres    false    215            �           2606    16752    groups groups_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (group_id);
 <   ALTER TABLE ONLY public.groups DROP CONSTRAINT groups_pkey;
       public            postgres    false    217            �           2606    16780    lecture lecture_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.lecture
    ADD CONSTRAINT lecture_pkey PRIMARY KEY (id_lecture);
 >   ALTER TABLE ONLY public.lecture DROP CONSTRAINT lecture_pkey;
       public            postgres    false    225            �           2606    16759    subjects subjects_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_pkey PRIMARY KEY (subject_id);
 @   ALTER TABLE ONLY public.subjects DROP CONSTRAINT subjects_pkey;
       public            postgres    false    219            �           2606    16766    teachers teachers_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.teachers
    ADD CONSTRAINT teachers_pkey PRIMARY KEY (teacher_id);
 @   ALTER TABLE ONLY public.teachers DROP CONSTRAINT teachers_pkey;
       public            postgres    false    221            �           2606    16997    users users_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (telegram_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    226           