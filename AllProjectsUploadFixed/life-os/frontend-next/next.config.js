module.exports = {
  reactStrictMode: true,
  async rewrites() {
    return [
      { source: '/api/ingest', destination: 'http://0.0.0.0:8000/ingest' },
      { source: '/api/search', destination: 'http://0.0.0.0:8000/search/' }
    ]
  }
}
