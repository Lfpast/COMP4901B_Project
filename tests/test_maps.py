#!/usr/bin/env python3
"""
Quick test script for Google Maps functionality.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools import google_maps_search, create_map_visualization

def main():
    print("Testing Google Maps Search...")
    print("-" * 50)
    
    # Test 1: Search for coffee shops
    print("\n1. Searching for coffee shops in Hong Kong...")
    result = google_maps_search(
        query="coffee shops",
        location="Central, Hong Kong",
        num=5
    )
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        print("\nMake sure your Serper-API key is set in .env file:")
        print("Serper-API=your_api_key_here")
        return
    
    print(f"✓ Found {len(result['places'])} places")
    
    # Display results
    for i, place in enumerate(result['places'], 1):
        print(f"\n  {i}. {place['title']}")
        print(f"     📍 {place['address']}")
        print(f"     ⭐ {place['rating']} ({place['reviews']} reviews)")
        print(f"     📂 {place['category']}")
    
    # Test 2: Create map visualization
    print("\n\n2. Creating map visualization...")
    map_result = create_map_visualization(
        places=result['places'],
        output_file="tests/test_coffee_map.html"
    )
    
    if "error" in map_result:
        print(f"❌ Error: {map_result['error']}")
    else:
        print(f"✓ Map created successfully!")
        print(f"   File: {map_result['file']}")
        print(f"   Markers: {map_result['num_markers']}")
        print(f"\n   🗺️  Open '{map_result['file']}' in your browser to view the map!")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    main()

