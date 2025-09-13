from app.supabase_client import supabase

def upload_bytes_to_storage(path: str, file_bytes: bytes, content_type: str = "application/octet-stream"):
    """Uploads file bytes to Supabase Storage (bucket: 'resumes') and returns a public/signed URL."""
    try:
        # Upload with overwrite (upsert=True)
        supabase.storage.from_("resumes").upload(
            path, file_bytes, {"content-type": content_type, "upsert": True}
        )

        # Try signed URL (valid 24 hours)
        signed = supabase.storage.from_("resumes").create_signed_url(path, 60 * 60 * 24)
        if signed and signed.get("signedURL"):
            return signed.get("signedURL")

        # Fallback to public URL if bucket is public
        public = supabase.storage.from_("resumes").get_public_url(path)
        return public.get("publicUrl") if public else path
    except Exception as e:
        raise RuntimeError(f"Upload failed: {e}")
