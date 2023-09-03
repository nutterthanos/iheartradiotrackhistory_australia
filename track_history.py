import asyncio
import aiohttp
import aiofiles
import logging
import json
import hashlib  # Import the hashlib module
import subprocess  # Import the subprocess module

# Set up logging
logging.basicConfig(level=logging.INFO)

async def download_track_history(sem: asyncio.Semaphore, station_id: int) -> None:
    logging.info(f"Starting download for Station ID: {station_id}")
    async with sem:
        while True:
            try:
                # Download track history for the given Station ID
                logging.info(f"Downloading track history for Station ID: {station_id}")
                async with aiohttp.ClientSession() as session:
                    api_url = f"https://au.api.iheart.com/api/v3/live-meta/stream/{station_id}/trackHistory?limit=10000"
                    async with session.get(api_url) as response:
                        if response.status == 200:
                            track_history = await response.text()
                            filename = f"trackhistory_{station_id}.json"
                            async with aiofiles.open(filename, "w", encoding='utf-8') as f:
                                await f.write(track_history)
                            logging.info(f"Download for Station ID: {station_id} completed")

                            # Calculate SHA-1 hash
                            sha1_hash = hashlib.sha1(track_history.encode('utf-8')).hexdigest()
                            sha1_filename = f"{station_id}.sha1"

                            # Save SHA-1 hash and filename with station ID
                            async with aiofiles.open(sha1_filename, "w", encoding='utf-8') as sha1_file:
                                await sha1_file.write(f"{sha1_hash} *{filename}")
                            logging.info(f"SHA-1 hash for Station ID: {station_id} saved")
                            
                        else:
                            logging.error(f"Failed to download track history for Station ID: {station_id}. Status code: {response.status}")
                break
            except Exception as e:
                logging.exception(f"Failed to download track history for Station ID: {station_id}, will retry in 5 seconds")
                await asyncio.sleep(5)

# Example usage:
async def main(station_ids):
    semaphore = asyncio.Semaphore(100)  # Limit concurrent downloads to 5 (adjust as needed)

    tasks = [download_track_history(semaphore, station_id) for station_id in station_ids]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    station_ids = [6157, 6176, 6177, 6178, 6179, 6180, 6181, 6182, 6183, 6184, 6185, 6186, 6243, 6244, 6308, 6309, 6310, 6311, 6312, 6313, 6314, 6315, 6316, 6317, 6318, 6319, 6320, 6321, 6322, 6323, 6324, 6325, 6326, 6327, 6328, 6329, 6330, 6331, 6332, 6333, 6334, 6336, 6441, 6460, 6461, 6492, 6585, 6700, 6702, 6708, 6709, 6713, 6714, 6728, 6793, 6794, 6902, 6914, 6917, 6923, 6935, 6941, 6998, 7025, 7028, 7029, 7030, 7031, 7050, 7075, 7090, 7093, 7110, 7111, 7112, 7115, 7116, 7118, 7123, 7124, 7125, 7126, 7127, 7128, 7129, 7130, 7131, 7132, 7133, 7134, 7135, 7136, 7137, 7138, 7139, 7140, 7141, 7142, 7143, 7144, 7145, 7146, 7147, 7148, 7149, 7172, 7176, 7177, 7178, 7179, 7180, 7181, 7182, 7183, 7184, 7185, 7186, 7187, 7222, 7308, 7421, 7547, 7967, 7968, 7969, 7970, 7971, 7972, 7973, 7974, 7975, 7976, 7977, 7978, 7979, 7980, 7981, 7982, 7983, 7984, 7985, 7986, 7987, 7988, 7989, 7990, 7991, 7992, 7993, 7994, 7995, 7996, 7997, 7998, 7999, 8000, 8001, 8002, 8003, 8004, 8005, 8325, 8326, 8327, 8328, 8329, 8330, 8331, 8332, 8333, 8334, 8336, 8377, 8525, 8603, 8665, 8670, 8674, 8675, 8676, 8677, 8708, 8736, 8809, 8841, 8863, 8865, 8866, 8876, 8877, 8878, 8879, 9024, 9025, 9026, 9027, 9028, 9029, 9030, 9031, 9032, 9033, 9037, 9038, 9039, 9040, 9041, 9042, 9043, 9044, 9045, 9046, 9047, 9048, 9056, 9105, 9106, 9107, 9176, 9177, 9195, 9243, 9245, 9246, 9247, 9248, 9249, 9250, 9262, 9263, 9264, 9265, 9266, 9267, 9268, 9269, 9270, 9271, 9272, 9273, 9274, 9275, 9276, 9277, 9278, 9279, 9280, 9281, 9282, 9283, 9284, 9285, 9286, 9287, 9288, 9289, 9290, 9291, 9292, 9293, 9294, 9295, 9296, 9297, 9298, 9299, 9300, 9301, 9302, 9303, 9304, 9305, 9306, 9307, 9308, 9309, 9310, 9311, 9312, 9313, 9314, 9315, 9333, 9334, 9353, 9363, 9364, 9365, 9366, 9367, 9368, 9369, 9370, 9371, 9372, 9373, 9374, 9381, 9382, 9383, 9394, 9395, 9434, 9435, 9436, 9437, 9438, 9440, 9460, 9474, 9482, 9522, 9555, 9592, 9593, 9594, 9595, 9596, 9597, 9598, 9599, 9600, 9616, 9621, 9630, 9631, 9641, 9642, 9660, 9661, 9680, 9687, 9688, 9689, 9690, 9696, 9697, 9713, 9714, 9735, 9748, 9749, 9750, 9783, 9786, 9787, 9809, 9885, 9892, 9893, 9917, 9931, 9932, 9933, 9934, 9935, 9939, 9942, 9943, 9944, 9945, 9946, 9947, 9948, 9949, 9950, 9951, 9952, 9981, 9984]  # Replace with your list of station IDs
    asyncio.run(main(station_ids))

    # After downloads are completed, run Git commands to add and commit
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', 'New Songs'])