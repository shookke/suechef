-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Families Table
CREATE TABLE families (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    family_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    family_id UUID REFERENCES families(id) ON DELETE CASCADE,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'member',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Preferences Table
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    dietary_restrictions JSONB DEFAULT '[]',
    allergies JSONB DEFAULT '[]',
    health_goals JSONB DEFAULT '[]',
    cuisine_likes JSONB DEFAULT '[]',
    cuisine_dislikes JSONB DEFAULT '[]',
    ingredient_dislikes JSONB DEFAULT '[]',
    cooking_skill_level VARCHAR(50),
    seasonal_preferences JSONB DEFAULT '[]',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Recipes Table
CREATE TABLE recipes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    instructions TEXT NOT NULL,
    image_url TEXT,
    prep_time_minutes INT,
    cook_time_minutes INT,
    serving_size INT DEFAULT 1,
    nutritional_info JSONB, -- Storing calories, protein, etc.
    cuisine_type VARCHAR(100),
    meal_type VARCHAR(100),
    tags TEXT[], -- Postgres Array for quick filtering
    original_url TEXT,
    source_type VARCHAR(50) NOT NULL DEFAULT 'internal',
    is_user_generated BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. Ingredients Master List
CREATE TABLE ingredients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) UNIQUE NOT NULL,
    common_unit VARCHAR(50),
    grocery_category VARCHAR(100) NOT NULL
);

-- 6. Recipe-Ingredient Mapping (The "Canonical" Recipe)
CREATE TABLE recipe_ingredients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recipe_id UUID REFERENCES recipes(id) ON DELETE CASCADE,
    ingredient_id UUID REFERENCES ingredients(id),
    quantity DECIMAL NOT NULL,
    unit_of_measure VARCHAR(50) NOT NULL,
    preparation_modifier TEXT
);

-- 7. User-Specific Recipe Customizations (Persistent alterations)
CREATE TABLE user_recipe_customizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    recipe_id UUID REFERENCES recipes(id) ON DELETE CASCADE,
    custom_ingredients JSONB NOT NULL, -- Overrides canonical recipe_ingredients
    custom_instructions TEXT,         -- Overrides canonical instructions
    UNIQUE(user_id, recipe_id)
);

-- 8. Weekly Menus
CREATE TABLE weekly_menus (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    family_id UUID REFERENCES families(id) ON DELETE CASCADE,
    week_start_date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(family_id, week_start_date)
);

-- 9. Daily Meals (The planned items for the week)
CREATE TABLE daily_meals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    weekly_menu_id UUID REFERENCES weekly_menus(id) ON DELETE CASCADE,
    recipe_id UUID REFERENCES recipes(id),
    day_of_week VARCHAR(20) NOT NULL,
    meal_slot_type VARCHAR(50) NOT NULL DEFAULT 'Dinner',
    user_notes TEXT,
    is_cooked BOOLEAN DEFAULT FALSE,
    is_skipped BOOLEAN DEFAULT FALSE
);