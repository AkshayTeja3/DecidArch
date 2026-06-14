from public_sphere import PublicSphere

# Run simulation
sphere = PublicSphere(num_receivers=100, num_sources=3, num_authorities=5, seed=None)
history = sphere.run_simulation(rounds=50, verbose=True)