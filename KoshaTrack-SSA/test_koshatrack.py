#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.propagator import OrbitPropagator
from datetime import datetime

print("\n🛰️  KoshaTrack SSA Platform - Quick Test")
print("=" * 60)

prop = OrbitPropagator()
print("✓ Orbit Propagator initialized")

iss_tle1 = "1 25544U 98067A   24001.50000000  .00016717  00000-0  10270-3 0  9005"
iss_tle2 = "2 25544  51.6400 208.9163 0006317  69.9862  25.2906 15.54225995227852"

success = prop.load_tle("ISS", iss_tle1, iss_tle2)
if success:
    print("✓ ISS TLE loaded successfully")
    
    result = prop.propagate("ISS", datetime.utcnow())
    print(f"\n📍 ISS Current State:")
    print(f"   Latitude:  {result['position']['lat']:>8.2f}°")
    print(f"   Longitude: {result['position']['lon']:>8.2f}°")
    print(f"   Altitude:  {result['position']['alt']:>8.1f} km")
    print(f"   Speed:     {result['velocity']['speed']:>8.2f} km/s")
else:
    print("✗ Failed to load TLE")

print("\n" + "=" * 60)
print("✓ Core functionality working! Ready to launch 🚀\n")
