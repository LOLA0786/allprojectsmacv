#!/usr/bin/env python3
"""Quick test of KoshaTrack"""

from src.core.propagator import OrbitPropagator
from datetime import datetime

print("🛰️ KoshaTrack Quick Test")
print("=" * 50)

prop = OrbitPropagator()
print("✓ Propagator initialized")

# ISS TLE
iss_tle1 = "1 25544U 98067A   24001.50000000  .00016717  00000-0  10270-3 0  9005"
iss_tle2 = "2 25544  51.6400 208.9163 0006317  69.9862  25.2906 15.54225995227852"

success = prop.load_tle("ISS", iss_tle1, iss_tle2)
if success:
    print("✓ ISS TLE loaded")
    result = prop.propagate("ISS", datetime.utcnow())
    print(f"✓ Position calculated: {result['position']}")
else:
    print("✗ Failed to load TLE")

print("=" * 50)
print("✓ Test complete! 🚀")
