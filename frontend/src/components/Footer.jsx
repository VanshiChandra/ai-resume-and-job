function Footer() {
  return (
    <footer className="bg-gray-800 text-gray-300 text-center py-4 mt-8">
      <p className="text-sm">
        © {new Date().getFullYear()} ResumeMatcher. All rights reserved.
      </p>
    </footer>
  );
}

export default Footer;
