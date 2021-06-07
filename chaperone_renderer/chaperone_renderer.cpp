#include "openvr.h"
#include <vector>
#include <fstream>
#include <iostream>
#include <cstdlib>

int main(int argc, char* argv[]) {

	int frameCount = atoi(argv[1]);
	std::cout << "frame count: " + std::to_string(frameCount) << std::endl;

	std::string frameDir = argv[2];
	std::cout << "frame directory: " + frameDir << std::endl;
	
	std::string frameName = argv[3];
	std::cout << "frame name: " + frameName << std::endl;

	vr::EVRInitError initError;
	vr::VR_Init(&initError, vr::EVRApplicationType::VRApplication_Scene);
	vr::VRChaperone()->GetCalibrationState();
	vr::VRChaperoneSetup()->RevertWorkingCopy();

	for (int x = 0; x < frameCount; x++) {
		std::string frame_path = frameDir + "/" + frameName + std::to_string(x) + ".txt";
		std::ifstream frameFile(frame_path, std::ios::in);
		std::vector<float> coordinates;
		if (!frameFile.is_open()) {
			std::cout << "failed to open file: " + frame_path << std::endl;
			exit(1);
		}
		double num = 0.0;
		while (frameFile >> num)
			coordinates.push_back(num);
		frameFile.close();

		int coordinateCount = std::floor(coordinates[0]);
		std::vector<vr::HmdQuad_t> quads(coordinateCount);

		for (int i = 0; i < coordinateCount; i++) {
			int k = i * 2;
			int thisX = k + 1.0;
			int thisZ = k + 2.0;
			quads[i].vCorners[0].v[0] = coordinates[thisX];
			quads[i].vCorners[0].v[1] = 0;
			quads[i].vCorners[0].v[2] = coordinates[thisZ];
			quads[i].vCorners[1].v[0] = coordinates[thisX];
			quads[i].vCorners[1].v[1] = 2.43f;
			quads[i].vCorners[1].v[2] = coordinates[thisZ];

			int j = (coordinateCount - 1) == i ? 0.0 : k + 2.0;
			int nextX = j + 1.0;
			int nextZ = j + 2.0;
			quads[i].vCorners[2].v[0] = coordinates[nextX];
			quads[i].vCorners[2].v[1] = 2.43f;
			quads[i].vCorners[2].v[2] = coordinates[nextZ];
			quads[i].vCorners[3].v[0] = coordinates[nextX];
			quads[i].vCorners[3].v[1] = 0;
			quads[i].vCorners[3].v[2] = coordinates[nextZ];
		}

		vr::VRChaperoneSetup()->SetWorkingCollisionBoundsInfo(quads.data(), coordinateCount);
		vr::VRChaperoneSetup()->CommitWorkingCopy(vr::EChaperoneConfigFile_Live);
	}
}