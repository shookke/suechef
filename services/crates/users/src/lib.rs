pub mod models;
pub mod security;

use models::{AuthResponse, CreateUserRequest, LoginRequest, User};
use security::{generate_token, hash_password, verify_password};
use sqlx::PgPool;
use uuid::Uuid;

pub struct UserManager {
    pool: PgPool,
    jwt_secret: String,
}

impl UserManager {
    pub fn new(pool: PgPool, jwt_secret: String) -> Self {
        Self { pool, jwt_secret }
    }

    /// Register a new user and optionally a new family
    pub async fn register(&self, req: CreateUserRequest) -> Result<AuthResponse, String> {
        let mut tx = self.pool.begin().await.map_err(|e: sqlx::Error| e.to_string())?;

        // 1. Handle Family Creation or Lookup
        // For MVP: Assuming creating a NEW family for every register if family_name is provided.
        // In future: Add logic to join existing family via invite code.
        let family_id = if let Some(name) = req.family_name {
            let fam_row: (Uuid,) = sqlx::query_as("INSERT INTO families (family_name) VALUES ($1) RETURNING id")
                .bind(name)
                .fetch_one(&mut *tx)
                .await
                .map_err(|e: sqlx::Error| format!("Failed to create family: {}", e))?;
            fam_row.0
        } else {
            return Err("Joining existing families not implemented yet".to_string());
        };

        // 2. Hash Password
        let hash = hash_password(&req.password).map_err(|_| "Password processing error".to_string())?;

        // 3. Create User
        let user: User = sqlx::query_as!(
            User,
            r#"
            INSERT INTO users (family_id, username, email, password_hash, role)
            VALUES ($1, $2, $3, $4, 'admin')
            RETURNING 
                id,
                family_id as "family_id!",
                username,
                email,
                password_hash,
                role,
                created_at,
                updated_at
            "#,
            family_id,
            req.username,
            req.email,
            hash,
        )
        .fetch_one(&mut *tx)
        .await
        .map_err(|e: sqlx::Error| format!("Failed to create user: {}", e))?;

        tx.commit().await.map_err(|e: sqlx::Error| e.to_string())?;

        // 4. Generate Token
        let token = generate_token(user.id, user.family_id, user.role.clone(), &self.jwt_secret)
            .map_err(|_| "Token generation failed".to_string())?;

        Ok(AuthResponse { token, user })
    }

    /// Authenticate a user
    pub async fn login(&self, req: LoginRequest) -> Result<AuthResponse, String> {
        let user: User = sqlx::query_as!(
            User,
            r#"SELECT 
                id, 
                family_id as "family_id!", 
                username, 
                email, 
                password_hash, 
                role, 
                created_at, 
                updated_at
            FROM users
            WHERE username = $1"#,
            req.username
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e: sqlx::Error| e.to_string())?
        .ok_or("User not found")?;

        if verify_password(&req.password, &user.password_hash) {
            let token = generate_token(user.id, user.family_id, user.role.clone(), &self.jwt_secret)
                .map_err(|_| "Token generation failed".to_string())?;
            Ok(AuthResponse { token, user })
        } else {
            Err("Invalid password".to_string())
        }
    }
}