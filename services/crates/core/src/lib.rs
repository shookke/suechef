use async_trait::async_trait;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

/// Core Recipe definition shared across all services.
#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Recipe {
    pub id: Uuid,
    pub name: String,
    pub original_url: Option<String>,
    pub ingredients: Vec<Ingredient>,
    pub instructions: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Ingredient {
    pub name: String,
    pub quantity: f64,
    pub unit: String,
    pub preparation: Option<String>,
}

/// Trait to allow SaaS vs Standalone provider implementations.
/// This allows us to easily swap Neo4j recommendations for 
/// a lightweight local SQL-based recommendation for Home Server users.
#[async_trait]
pub trait RecommendationProvider {
    async fn get_recommendations_for_user(&self, user_id: Uuid) -> Vec<Uuid>;
}

/// Trait for Inventory tracking.
/// Future implementations can target Smart Fridges (LG/Samsung APIs) 
/// or Matter-enabled pantry scales.
#[async_trait]
pub trait PantryProvider {
    async fn get_inventory(&self, family_id: Uuid) -> Vec<Ingredient>;
    async fn mark_as_used(&self, ingredient_id: Uuid, quantity: f64);
}

/// Common authentication response
#[derive(Debug, Serialize, Deserialize)]
pub struct AuthClaims {
    pub sub: Uuid,     // User ID
    pub fam: Uuid,     // Family ID
    pub role: String,  // RBAC Role
    pub exp: usize,
}