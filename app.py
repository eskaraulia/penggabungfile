import streamlit as st
from PIL import Image
import io
from pypdf import PdfWriter

st.set_page_config(page_title="Tools File Praktis", page_icon="🛠️")

st.title("🛠️ Kompresor & Konverter File")
st.write("Alat bantu praktis untuk kebutuhan tugas sekolah (Gambar & PDF).")

tab1, tab2 = st.tabs(["🖼️ Ubah & Kompres Gambar", "📄 Gabung PDF (PDF Merger)"])

# ------------------- TAB 1: UBAH & KOMPRES GAMBAR -------------------
with tab1:
    st.header("Pengolah Gambar")
    
    uploaded_image = st.file_uploader("Unggah gambar (PNG/JPG/JPEG/WebP):", type=["png", "jpg", "jpeg", "webp"])
    
    if uploaded_image is not None:
        img = Image.open(uploaded_image)
        st.image(img, caption="Gambar Asli", width=300)
        
        col1, col2 = st.columns(2)
        with col1:
            output_format = st.selectbox("Pilih Format Baru:", ["JPEG", "PNG", "WEBP"])
        with col2:
            quality = st.slider("Kualitas Gambar (%):", min_value=10, max_value=100, value=70)
            
        if st.button("Proses Gambar"):
            # Konversi mode warna jika format output JPEG (karena JPEG tidak mendukung transparansi/RGBA)
            img_converted = img.copy()
            if output_format == "JPEG" and img_converted.mode in ("RGBA", "P"):
                img_converted = img_converted.convert("RGB")
                
            buf = io.BytesIO()
            img_converted.save(buf, format=output_format, quality=quality, optimize=True)
            byte_im = buf.getvalue()
            
            # Hitung ukuran file
            ukuran_lama = len(uploaded_image.getvalue()) / 1024
            ukuran_baru = len(byte_im) / 1024
            
            st.success(f"🎉 Berhasil! Ukuran awal: {ukuran_lama:.1f} KB ➔ Ukuran baru: {ukuran_baru:.1f} KB")
            
            ext = output_format.lower()
            if ext == "jpeg":
                ext = "jpg"
                
            st.download_button(
                label=f"📥 Download Gambar ({output_format})",
                data=byte_im,
                file_name=f"hasil_konversi.{ext}",
                mime=f"image/{ext}"
            )

# ------------------- TAB 2: GABUNG PDF -------------------
with tab2:
    st.header("Penggabung File PDF")
    
    uploaded_pdfs = st.file_uploader("Unggah 2 atau lebih file PDF:", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_pdfs:
        if len(uploaded_pdfs) < 2:
            st.warning("Unggah minimal 2 file PDF untuk digabungkan.")
        else:
            st.write(f"Terpilih **{len(uploaded_pdfs)}** file PDF:")
            for idx, pdf in enumerate(uploaded_pdfs, 1):
                st.write(f"{idx}. {pdf.name}")
                
            if st.button("🔗 Gabungkan PDF"):
                merger = PdfWriter()
                
                for pdf in uploaded_pdfs:
                    merger.append(pdf)
                    
                output_pdf = io.BytesIO()
                merger.write(output_pdf)
                merger.close()
                
                st.success("🎉 PDF berhasil digabungkan!")
                st.download_button(
                    label="📥 Download PDF Gabungan",
                    data=output_pdf.getvalue(),
                    file_name="pdf_gabungan.pdf",
                    mime="application/pdf"
                )