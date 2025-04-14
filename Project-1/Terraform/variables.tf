variable "external_id" {
  type      = string
  sensitive = true
}
variable "assume_role" {
  type      = string
  sensitive = true
  description = "put role ARN"
}
variable "user_arn" {
   type      = string
  sensitive = true 
  description = "put user ARN"
  
}