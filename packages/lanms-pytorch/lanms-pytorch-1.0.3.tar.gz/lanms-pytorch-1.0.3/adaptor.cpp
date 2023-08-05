#include <torch/script.h>
#include "lanms.h"

namespace lanms_adaptor {

	std::vector<std::array<double, 9>> polys2doubles(const std::vector<lanms::Polygon> &polys) {
		std::vector<std::array<double, 9>> ret;
		ret.reserve(polys.size());
		for (size_t i = 0; i < polys.size(); i ++) {
			auto &p = polys[i];
			auto &poly = p.poly;
			ret.push_back({
					double(poly[0].X), double(poly[0].Y),
					double(poly[1].X), double(poly[1].Y),
					double(poly[2].X), double(poly[2].Y),
					double(poly[3].X), double(poly[3].Y),
					double(p.score),
					});
		}

		return ret;
	}


	/**
	 *
	 * \param quad_n9 an n-by-9 numpy array, where first 8 numbers denote the
	 *		quadrangle, and the last one is the score
	 * \param iou_threshold two quadrangles with iou score above this threshold
	 *		will be merged
	 *
	 * \return an n-by-9 numpy array, the merged quadrangles
	 */
	torch::Tensor merge_quadrangle_n9(torch::Tensor quad_n9, double iou_threshold) {
		const auto &shape = quad_n9.sizes();
		if (shape.size() != 2 || shape[1] != 9)
			throw std::runtime_error("quadrangles must have a shape of (n, 9)");
		auto n = shape[0];
		auto ptr = quad_n9.data_ptr<double>();
		auto polys = polys2doubles(lanms::merge_quadrangle_n9(ptr, n, iou_threshold));
		return torch::from_blob(polys.data(), { static_cast<int>(polys.size()), 9 }, at::kDouble).clone();
	}

}

TORCH_LIBRARY(lanms, m) {
	m.def("merge_quadrangle_n9", lanms_adaptor::merge_quadrangle_n9);
}

